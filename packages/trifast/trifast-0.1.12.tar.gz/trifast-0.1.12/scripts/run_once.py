"""
Simple script to run individual Triton kernels once with configurable parameters.
Designed to be used with NVIDIA Nsight Compute (NCU) CLI profiler.

Example usage:
    ncu -o profile_result --set full python ncu_kernel_runner.py --kernel fwd --h 8 --n 256 --d 64
"""

import os
import sys
import argparse
import torch
import triton
from einops import rearrange


def setup_tensors(h, n, d, b=1, device="cuda", dtype=torch.float16):
    """
    Create tensors with appropriate shapes for all kernels.

    Args:
        h: Number of heads
        n: Sequence length
        d: Embedding dimension
        b: Batch size
        device: Device to run on
        dtype: Data type for tensors

    Returns:
        Dict containing all tensors needed for the kernels
    """
    # Create original tensors in batch,head format
    q_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    k_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    v_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    bias_orig = torch.randn(b, h, n, n, device=device, dtype=dtype).contiguous()
    o_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    do_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()

    # Flatten batch and head dimensions
    q = rearrange(q_orig, "b h ... -> (b h) ...").contiguous()
    k = rearrange(k_orig, "b h ... -> (b h) ...").contiguous()
    v = rearrange(v_orig, "b h ... -> (b h) ...").contiguous()
    bias = rearrange(bias_orig, "b h ... -> (b h) ...").contiguous()
    o = rearrange(o_orig, "b h ... -> (b h) ...").contiguous()
    do = rearrange(do_orig, "b h ... -> (b h) ...").contiguous()

    # Create other tensors
    lse = torch.zeros((b*h, n, n), device=device, dtype=torch.float32).contiguous()
    mask = torch.zeros(b, n, n, device=device, dtype=torch.bool).contiguous()

    # Output tensors for backward kernels
    d_tensor = torch.zeros((b*h, n, n), dtype=dtype, device=device)
    dq = torch.zeros_like(q)
    dk = torch.zeros_like(k)
    dv = torch.zeros_like(v)
    db = torch.zeros_like(bias)

    # Output tensor for forward kernel (used by triton kernel)
    o_out = torch.zeros_like(q)

    # Prepare common parameters
    sm_scale = q.shape[-1] ** -0.5
    neg_inf = torch.finfo(dtype).min

    return {
        "q": q,
        "k": k,
        "v": v,
        "bias": bias,
        "o": o,
        "do": do,
        "lse": lse,
        "mask": mask,
        "d_tensor": d_tensor,
        "dq": dq,
        "dk": dk,
        "dv": dv,
        "db": db,
        "o_out": o_out,
        "sm_scale": sm_scale,
        "neg_inf": neg_inf,
        "bh": b * h,
    }


def run_fwd_kernel(tensors, h, n, d):
    """Run the forward kernel once."""
    from trifast.triton import _fwd

    # Grid for triton kernel
    def grid(x):
        return (triton.cdiv(n, x["BLOCK_J"]), n, tensors["bh"])

    # Run the kernel once
    _fwd[grid](
        tensors["o_out"], tensors["o_out"].stride(0), tensors["o_out"].stride(1),
        tensors["o_out"].stride(2), tensors["o_out"].stride(3),
        tensors["lse"], tensors["lse"].stride(0), tensors["lse"].stride(1), tensors["lse"].stride(2),
        tensors["q"], tensors["q"].stride(0), tensors["q"].stride(1),
        tensors["q"].stride(2), tensors["q"].stride(3),
        tensors["k"], tensors["k"].stride(0), tensors["k"].stride(1),
        tensors["k"].stride(2), tensors["k"].stride(3),
        tensors["v"], tensors["v"].stride(0), tensors["v"].stride(1),
        tensors["v"].stride(2), tensors["v"].stride(3),
        tensors["bias"], tensors["bias"].stride(0), tensors["bias"].stride(1), tensors["bias"].stride(2),
        tensors["mask"], tensors["mask"].stride(0), tensors["mask"].stride(1), tensors["mask"].stride(2),
        neg_inf=tensors["neg_inf"],
        sm_scale=tensors["sm_scale"], N=n, H=h, DIM=d,
    )

    # Make sure kernel finishes
    torch.cuda.synchronize()

    return "Forward kernel completed"


def run_bwd_q_kernel(tensors, h, n, d):
    """Run the backward Q kernel once."""
    from trifast.triton import _bwd_q

    # Grid for triton kernel
    def q_grid(x):
        return (triton.cdiv(n, x["BLOCK_J"]), n, tensors["bh"])

    # Run the kernel once
    _bwd_q[q_grid](
        tensors["d_tensor"], tensors["d_tensor"].stride(0), tensors["d_tensor"].stride(1),
        tensors["d_tensor"].stride(2),
        tensors["q"], tensors["q"].stride(0), tensors["q"].stride(1),
        tensors["q"].stride(2), tensors["q"].stride(3),
        tensors["k"], tensors["k"].stride(0), tensors["k"].stride(1),
        tensors["k"].stride(2), tensors["k"].stride(3),
        tensors["v"], tensors["v"].stride(0), tensors["v"].stride(1),
        tensors["v"].stride(2), tensors["v"].stride(3),
        tensors["bias"], tensors["bias"].stride(0), tensors["bias"].stride(1), tensors["bias"].stride(2),
        tensors["lse"], tensors["lse"].stride(0), tensors["lse"].stride(1), tensors["lse"].stride(2),
        tensors["mask"], tensors["mask"].stride(0), tensors["mask"].stride(1), tensors["mask"].stride(2),
        tensors["o"], tensors["o"].stride(0), tensors["o"].stride(1),
        tensors["o"].stride(2), tensors["o"].stride(3),
        tensors["do"], tensors["do"].stride(0), tensors["do"].stride(1),
        tensors["do"].stride(2), tensors["do"].stride(3),
        tensors["dq"], tensors["dq"].stride(0), tensors["dq"].stride(1),
        tensors["dq"].stride(2), tensors["dq"].stride(3),
        sm_scale=tensors["sm_scale"],
        neg_inf=tensors["neg_inf"],
        H=h, N=n, DIM=d,
    )

    # Make sure kernel finishes
    torch.cuda.synchronize()
    return "Backward Q kernel completed"


def run_bwd_kv_kernel(tensors, h, n, d):
    """Run the backward KV kernel once."""
    from trifast.triton import _bwd_kv

    # Grid for triton kernel
    def kv_grid(x):
        return (triton.cdiv(n, x["BLOCK_K"]), n, tensors["bh"])

    # Run the kernel once
    _bwd_kv[kv_grid](
        tensors["d_tensor"], tensors["d_tensor"].stride(0), tensors["d_tensor"].stride(1),
        tensors["d_tensor"].stride(2),
        tensors["q"], tensors["q"].stride(0), tensors["q"].stride(1),
        tensors["q"].stride(2), tensors["q"].stride(3),
        tensors["k"], tensors["k"].stride(0), tensors["k"].stride(1),
        tensors["k"].stride(2), tensors["k"].stride(3),
        tensors["v"], tensors["v"].stride(0), tensors["v"].stride(1),
        tensors["v"].stride(2), tensors["v"].stride(3),
        tensors["bias"], tensors["bias"].stride(0), tensors["bias"].stride(1), tensors["bias"].stride(2),
        tensors["lse"], tensors["lse"].stride(0), tensors["lse"].stride(1), tensors["lse"].stride(2),
        tensors["mask"], tensors["mask"].stride(0), tensors["mask"].stride(1), tensors["mask"].stride(2),
        tensors["do"], tensors["do"].stride(0), tensors["do"].stride(1),
        tensors["do"].stride(2), tensors["do"].stride(3),
        tensors["dk"], tensors["dk"].stride(0), tensors["dk"].stride(1),
        tensors["dk"].stride(2), tensors["dk"].stride(3),
        tensors["dv"], tensors["dv"].stride(0), tensors["dv"].stride(1),
        tensors["dv"].stride(2), tensors["dv"].stride(3),
        sm_scale=tensors["sm_scale"],
        neg_inf=tensors["neg_inf"],
        H=h, N=n, DIM=d,
    )

    # Make sure kernel finishes
    torch.cuda.synchronize()
    return "Backward KV kernel completed"


def run_bwd_b_kernel(tensors, h, n, d):
    """Run the backward bias kernel once."""
    from trifast.triton import _bwd_b

    # Grid for triton kernel
    def b_grid(x):
        return (
            triton.cdiv(n, x["BLOCK_J"]),
            triton.cdiv(n, x["BLOCK_K"]),
            tensors["bh"],
        )

    # Run the kernel once
    _bwd_b[b_grid](
        tensors["d_tensor"], tensors["d_tensor"].stride(0), tensors["d_tensor"].stride(1),
        tensors["d_tensor"].stride(2),
        tensors["q"], tensors["q"].stride(0), tensors["q"].stride(1),
        tensors["q"].stride(2), tensors["q"].stride(3),
        tensors["k"], tensors["k"].stride(0), tensors["k"].stride(1),
        tensors["k"].stride(2), tensors["k"].stride(3),
        tensors["v"], tensors["v"].stride(0), tensors["v"].stride(1),
        tensors["v"].stride(2), tensors["v"].stride(3),
        tensors["bias"], tensors["bias"].stride(0), tensors["bias"].stride(1), tensors["bias"].stride(2),
        tensors["lse"], tensors["lse"].stride(0), tensors["lse"].stride(1), tensors["lse"].stride(2),
        tensors["mask"], tensors["mask"].stride(0), tensors["mask"].stride(1), tensors["mask"].stride(2),
        tensors["do"], tensors["do"].stride(0), tensors["do"].stride(1),
        tensors["do"].stride(2), tensors["do"].stride(3),
        tensors["db"], tensors["db"].stride(0), tensors["db"].stride(1), tensors["db"].stride(2),
        sm_scale=tensors["sm_scale"],
        neg_inf=tensors["neg_inf"],
        H=h, N=n, DIM=d,
    )

    # Make sure kernel finishes
    torch.cuda.synchronize()
    return "Backward bias kernel completed"


def main():
    parser = argparse.ArgumentParser(description='Run Triton kernels for NCU profiling')
    parser.add_argument('--kernel', type=str, required=True,
                      choices=['fwd', 'bwd_q', 'bwd_kv', 'bwd_b', 'all'],
                      help='Which kernel to run: fwd, bwd_q, bwd_kv, bwd_b, or all')
    parser.add_argument('--h', type=int, default=8, help='Number of heads')
    parser.add_argument('--n', type=int, default=128, help='Sequence length')
    parser.add_argument('--d', type=int, default=64, help='Embedding dimension')
    parser.add_argument('--b', type=int, default=1, help='Batch size')
    parser.add_argument('--dtype', type=str, default='bfloat16',
                      choices=['float16', 'float32', 'bfloat16'],
                      help='Data type for tensors')

    args = parser.parse_args()

    # Map string dtype to torch dtype
    dtype_map = {
        'float16': torch.float16,
        'float32': torch.float32,
        'bfloat16': torch.bfloat16,
    }

    # Create tensors
    tensors = setup_tensors(
        h=args.h,
        n=args.n,
        d=args.d,
        b=args.b,
        dtype=dtype_map[args.dtype]
    )

    # Run the selected kernel(s)
    if args.kernel == 'fwd' or args.kernel == 'all':
        print(run_fwd_kernel(tensors, args.h, args.n, args.d))

    if args.kernel == 'bwd_q' or args.kernel == 'all':
        print(run_bwd_q_kernel(tensors, args.h, args.n, args.d))

    if args.kernel == 'bwd_kv' or args.kernel == 'all':
        print(run_bwd_kv_kernel(tensors, args.h, args.n, args.d))

    if args.kernel == 'bwd_b' or args.kernel == 'all':
        print(run_bwd_b_kernel(tensors, args.h, args.n, args.d))


if __name__ == "__main__":
    main()
