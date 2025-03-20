import triton
import torch
import time
import numpy as np
from typing import Dict, Any
from einops import rearrange


def profile_fwd_kernel(
    h: int = 8,
    n: int = 128,
    d: int = 64,
    device="cuda",
    dtype=torch.bfloat16,
    num_warmup=10,
    num_repeats=100,
) -> Dict[str, Any]:
    """
    Profile the forward kernel (_fwd) independently.

    Args:
        h: Number of heads
        n: Sequence length
        d: Embedding dimension
        device: Device to run on
        dtype: Data type for tensors
        num_warmup: Number of warmup iterations
        num_repeats: Number of iterations to measure

    Returns:
        Dict with profiling results
    """
    # Generate tensors with appropriate shapes
    b = 1  # Batch size 1 for profiling
    q = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    k = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    v = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    bias = torch.randn(b, h, n, n, device=device, dtype=dtype).contiguous()
    mask = torch.zeros(b, n, n, device=device, dtype=torch.bool).contiguous()

    # Create output tensors
    o = torch.zeros_like(q)

    # Flatten batch and head dimensions for triton
    q_flat = rearrange(q, "b h ... -> (b h) ...").contiguous()
    k_flat = rearrange(k, "b h ... -> (b h) ...").contiguous()
    v_flat = rearrange(v, "b h ... -> (b h) ...").contiguous()
    b_flat = rearrange(bias, "b h ... -> (b h) ...").contiguous()
    o_flat = rearrange(o, "b h ... -> (b h) ...").contiguous()

    # Create LSE tensor in the flattened shape
    bh = b * h
    lse = torch.zeros((bh, n, n), device=device, dtype=torch.float32).contiguous()

    # Prepare for triton
    sm_scale = q.shape[-1] ** -0.5
    neg_inf = torch.finfo(dtype).min

    # Grid for triton kernel
    def grid(x):
        return (triton.cdiv(n, x["BLOCK_J"]), n, bh)

    # Warmup
    for _ in range(num_warmup):
        from trifast.triton import _fwd

        _fwd[grid](
            o_flat,
            o_flat.stride(0),
            o_flat.stride(1),
            o_flat.stride(2),
            o_flat.stride(3),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            q_flat,
            q_flat.stride(0),
            q_flat.stride(1),
            q_flat.stride(2),
            q_flat.stride(3),
            k_flat,
            k_flat.stride(0),
            k_flat.stride(1),
            k_flat.stride(2),
            k_flat.stride(3),
            v_flat,
            v_flat.stride(0),
            v_flat.stride(1),
            v_flat.stride(2),
            v_flat.stride(3),
            b_flat,
            b_flat.stride(0),
            b_flat.stride(1),
            b_flat.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            neg_inf=neg_inf,
            sm_scale=sm_scale,
            N=n,
            H=h,
            DIM=d,
        )

    # Measure performance with per-iteration timing
    times_ms = []

    for _ in range(num_repeats):
        # Synchronize before measuring each iteration
        torch.cuda.synchronize()
        start = time.time()

        from trifast.triton import _fwd

        _fwd[grid](
            o_flat,
            o_flat.stride(0),
            o_flat.stride(1),
            o_flat.stride(2),
            o_flat.stride(3),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            q_flat,
            q_flat.stride(0),
            q_flat.stride(1),
            q_flat.stride(2),
            q_flat.stride(3),
            k_flat,
            k_flat.stride(0),
            k_flat.stride(1),
            k_flat.stride(2),
            k_flat.stride(3),
            v_flat,
            v_flat.stride(0),
            v_flat.stride(1),
            v_flat.stride(2),
            v_flat.stride(3),
            b_flat,
            b_flat.stride(0),
            b_flat.stride(1),
            b_flat.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            neg_inf=neg_inf,
            sm_scale=sm_scale,
            N=n,
            H=h,
            DIM=d,
        )

        # Synchronize after each iteration to get accurate timing
        torch.cuda.synchronize()
        end = time.time()
        times_ms.append((end - start) * 1000)

    # Calculate statistics
    times_ms_array = np.array(times_ms)
    avg_time_ms = np.mean(times_ms_array)
    std_time_ms = np.std(times_ms_array)

    return {
        "kernel": "_fwd",
        "h": h,
        "n": n,
        "d": d,
        "avg_time_ms": float(avg_time_ms),
        "std_time_ms": float(std_time_ms),
        "min_time_ms": float(np.min(times_ms_array)),
        "max_time_ms": float(np.max(times_ms_array)),
        "iterations": num_repeats,
        "all_times_ms": times_ms,
    }


def profile_bwd_q_kernel(
    h: int = 8,
    n: int = 128,
    d: int = 64,
    device="cuda",
    dtype=torch.bfloat16,
    num_warmup=10,
    num_repeats=100,
) -> Dict[str, Any]:
    """
    Profile the backward Q kernel (_bwd_q) independently.

    Args:
        h: Number of heads
        n: Sequence length
        d: Embedding dimension
        device: Device to run on
        dtype: Data type for tensors
        num_warmup: Number of warmup iterations
        num_repeats: Number of iterations to measure

    Returns:
        Dict with profiling results
    """
    # Generate tensors with appropriate shapes
    b = 1  # Batch size 1 for profiling

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
    lse = torch.randn(b * h, n, n, device=device, dtype=torch.float32).contiguous()
    mask = torch.zeros(b, n, n, device=device, dtype=torch.bool).contiguous()

    # Create output tensors
    d_tensor = torch.zeros((b * h, n, n), dtype=dtype, device=device)
    dq = torch.zeros_like(q)

    # Prepare for triton
    sm_scale = q.shape[-1] ** -0.5
    neg_inf = torch.finfo(dtype).min

    # Grid for triton kernel
    def q_grid(x):
        return (triton.cdiv(n, x["BLOCK_J"]), n, b * h)

    # Warmup
    for _ in range(num_warmup):
        from trifast.triton import _bwd_q

        _bwd_q[q_grid](
            d_tensor,
            d_tensor.stride(0),
            d_tensor.stride(1),
            d_tensor.stride(2),
            q,
            q.stride(0),
            q.stride(1),
            q.stride(2),
            q.stride(3),
            k,
            k.stride(0),
            k.stride(1),
            k.stride(2),
            k.stride(3),
            v,
            v.stride(0),
            v.stride(1),
            v.stride(2),
            v.stride(3),
            bias,
            bias.stride(0),
            bias.stride(1),
            bias.stride(2),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            o,
            o.stride(0),
            o.stride(1),
            o.stride(2),
            o.stride(3),
            do,
            do.stride(0),
            do.stride(1),
            do.stride(2),
            do.stride(3),
            dq,
            dq.stride(0),
            dq.stride(1),
            dq.stride(2),
            dq.stride(3),
            sm_scale=sm_scale,
            neg_inf=neg_inf,
            H=h,
            N=n,
            DIM=d,
        )

    # Measure performance with per-iteration timing
    times_ms = []

    for _ in range(num_repeats):
        # Synchronize before measuring each iteration
        torch.cuda.synchronize()
        start = time.time()

        from trifast.triton import _bwd_q

        _bwd_q[q_grid](
            d_tensor,
            d_tensor.stride(0),
            d_tensor.stride(1),
            d_tensor.stride(2),
            q,
            q.stride(0),
            q.stride(1),
            q.stride(2),
            q.stride(3),
            k,
            k.stride(0),
            k.stride(1),
            k.stride(2),
            k.stride(3),
            v,
            v.stride(0),
            v.stride(1),
            v.stride(2),
            v.stride(3),
            bias,
            bias.stride(0),
            bias.stride(1),
            bias.stride(2),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            o,
            o.stride(0),
            o.stride(1),
            o.stride(2),
            o.stride(3),
            do,
            do.stride(0),
            do.stride(1),
            do.stride(2),
            do.stride(3),
            dq,
            dq.stride(0),
            dq.stride(1),
            dq.stride(2),
            dq.stride(3),
            sm_scale=sm_scale,
            neg_inf=neg_inf,
            H=h,
            N=n,
            DIM=d,
        )

        # Synchronize after each iteration to get accurate timing
        torch.cuda.synchronize()
        end = time.time()
        times_ms.append((end - start) * 1000)

    # Calculate statistics
    times_ms_array = np.array(times_ms)
    avg_time_ms = np.mean(times_ms_array)
    std_time_ms = np.std(times_ms_array)

    return {
        "kernel": "_bwd_q",
        "h": h,
        "n": n,
        "d": d,
        "avg_time_ms": float(avg_time_ms),
        "std_time_ms": float(std_time_ms),
        "min_time_ms": float(np.min(times_ms_array)),
        "max_time_ms": float(np.max(times_ms_array)),
        "iterations": num_repeats,
        "all_times_ms": times_ms,
    }


def profile_bwd_kv_kernel(
    h: int = 8,
    n: int = 128,
    d: int = 64,
    device="cuda",
    dtype=torch.bfloat16,
    num_warmup=10,
    num_repeats=100,
) -> Dict[str, Any]:
    """
    Profile the backward KV kernel (_bwd_kv) independently.

    Args:
        h: Number of heads
        n: Sequence length
        d: Embedding dimension
        device: Device to run on
        dtype: Data type for tensors
        num_warmup: Number of warmup iterations
        num_repeats: Number of iterations to measure

    Returns:
        Dict with profiling results
    """
    # Generate tensors with appropriate shapes
    b = 1  # Batch size 1 for profiling

    # Create original tensors in batch,head format
    q_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    k_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    v_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    bias_orig = torch.randn(b, h, n, n, device=device, dtype=dtype).contiguous()
    do_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()

    # Flatten batch and head dimensions
    q = rearrange(q_orig, "b h ... -> (b h) ...").contiguous()
    k = rearrange(k_orig, "b h ... -> (b h) ...").contiguous()
    v = rearrange(v_orig, "b h ... -> (b h) ...").contiguous()
    bias = rearrange(bias_orig, "b h ... -> (b h) ...").contiguous()
    do = rearrange(do_orig, "b h ... -> (b h) ...").contiguous()

    # Create other tensors
    d_tensor = torch.randn(b * h, n, n, device=device, dtype=dtype).contiguous()
    lse = torch.randn(b * h, n, n, device=device, dtype=torch.float32).contiguous()
    mask = torch.zeros(b, n, n, device=device, dtype=torch.bool).contiguous()

    # Create output tensors
    dk = torch.zeros_like(k)
    dv = torch.zeros_like(v)

    # Prepare for triton
    sm_scale = q.shape[-1] ** -0.5
    neg_inf = torch.finfo(dtype).min

    # Grid for triton kernel
    def kv_grid(x):
        return (triton.cdiv(n, x["BLOCK_K"]), n, b * h)

    # Warmup
    for _ in range(num_warmup):
        from trifast.triton import _bwd_kv

        _bwd_kv[kv_grid](
            d_tensor,
            d_tensor.stride(0),
            d_tensor.stride(1),
            d_tensor.stride(2),
            q,
            q.stride(0),
            q.stride(1),
            q.stride(2),
            q.stride(3),
            k,
            k.stride(0),
            k.stride(1),
            k.stride(2),
            k.stride(3),
            v,
            v.stride(0),
            v.stride(1),
            v.stride(2),
            v.stride(3),
            bias,
            bias.stride(0),
            bias.stride(1),
            bias.stride(2),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            do,
            do.stride(0),
            do.stride(1),
            do.stride(2),
            do.stride(3),
            dk,
            dk.stride(0),
            dk.stride(1),
            dk.stride(2),
            dk.stride(3),
            dv,
            dv.stride(0),
            dv.stride(1),
            dv.stride(2),
            dv.stride(3),
            sm_scale=sm_scale,
            neg_inf=neg_inf,
            H=h,
            N=n,
            DIM=d,
        )

    # Measure performance with per-iteration timing
    times_ms = []

    for _ in range(num_repeats):
        # Synchronize before measuring each iteration
        torch.cuda.synchronize()
        start = time.time()

        from trifast.triton import _bwd_kv

        _bwd_kv[kv_grid](
            d_tensor,
            d_tensor.stride(0),
            d_tensor.stride(1),
            d_tensor.stride(2),
            q,
            q.stride(0),
            q.stride(1),
            q.stride(2),
            q.stride(3),
            k,
            k.stride(0),
            k.stride(1),
            k.stride(2),
            k.stride(3),
            v,
            v.stride(0),
            v.stride(1),
            v.stride(2),
            v.stride(3),
            bias,
            bias.stride(0),
            bias.stride(1),
            bias.stride(2),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            do,
            do.stride(0),
            do.stride(1),
            do.stride(2),
            do.stride(3),
            dk,
            dk.stride(0),
            dk.stride(1),
            dk.stride(2),
            dk.stride(3),
            dv,
            dv.stride(0),
            dv.stride(1),
            dv.stride(2),
            dv.stride(3),
            sm_scale=sm_scale,
            neg_inf=neg_inf,
            H=h,
            N=n,
            DIM=d,
        )

        # Synchronize after each iteration to get accurate timing
        torch.cuda.synchronize()
        end = time.time()
        times_ms.append((end - start) * 1000)

    # Calculate statistics
    times_ms_array = np.array(times_ms)
    avg_time_ms = np.mean(times_ms_array)
    std_time_ms = np.std(times_ms_array)

    return {
        "kernel": "_bwd_kv",
        "h": h,
        "n": n,
        "d": d,
        "avg_time_ms": float(avg_time_ms),
        "std_time_ms": float(std_time_ms),
        "min_time_ms": float(np.min(times_ms_array)),
        "max_time_ms": float(np.max(times_ms_array)),
        "iterations": num_repeats,
        "all_times_ms": times_ms,
    }


def profile_bwd_b_kernel(
    h: int = 8,
    n: int = 128,
    d: int = 64,
    device="cuda",
    dtype=torch.bfloat16,
    num_warmup=10,
    num_repeats=100,
) -> Dict[str, Any]:
    """
    Profile the backward bias kernel (_bwd_b) independently.

    Args:
        h: Number of heads
        n: Sequence length
        d: Embedding dimension
        device: Device to run on
        dtype: Data type for tensors
        num_warmup: Number of warmup iterations
        num_repeats: Number of iterations to measure

    Returns:
        Dict with profiling results
    """
    # Generate tensors with appropriate shapes
    b = 1  # Batch size 1 for profiling

    # Create original tensors in batch,head format
    q_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    k_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    v_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()
    bias_orig = torch.randn(b, h, n, n, device=device, dtype=dtype).contiguous()
    do_orig = torch.randn(b, h, n, n, d, device=device, dtype=dtype).contiguous()

    # Flatten batch and head dimensions
    q = rearrange(q_orig, "b h ... -> (b h) ...").contiguous()
    k = rearrange(k_orig, "b h ... -> (b h) ...").contiguous()
    v = rearrange(v_orig, "b h ... -> (b h) ...").contiguous()
    bias = rearrange(bias_orig, "b h ... -> (b h) ...").contiguous()
    do = rearrange(do_orig, "b h ... -> (b h) ...").contiguous()

    # Create other tensors
    d_tensor = torch.randn(b * h, n, n, device=device, dtype=dtype).contiguous()
    lse = torch.randn(b * h, n, n, device=device, dtype=torch.float32).contiguous()
    mask = torch.zeros(b, n, n, device=device, dtype=torch.bool).contiguous()

    # Create output tensors
    db = torch.zeros_like(bias)

    # Prepare for triton
    sm_scale = q.shape[-1] ** -0.5
    neg_inf = torch.finfo(dtype).min

    # Grid for triton kernel
    def b_grid(x):
        return (
            triton.cdiv(n, x["BLOCK_J"]),
            triton.cdiv(n, x["BLOCK_K"]),
            b * h,
        )

    # Warmup
    for _ in range(num_warmup):
        from trifast.triton import _bwd_b

        _bwd_b[b_grid](
            d_tensor,
            d_tensor.stride(0),
            d_tensor.stride(1),
            d_tensor.stride(2),
            q,
            q.stride(0),
            q.stride(1),
            q.stride(2),
            q.stride(3),
            k,
            k.stride(0),
            k.stride(1),
            k.stride(2),
            k.stride(3),
            v,
            v.stride(0),
            v.stride(1),
            v.stride(2),
            v.stride(3),
            bias,
            bias.stride(0),
            bias.stride(1),
            bias.stride(2),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            do,
            do.stride(0),
            do.stride(1),
            do.stride(2),
            do.stride(3),
            db,
            db.stride(0),
            db.stride(1),
            db.stride(2),
            sm_scale=sm_scale,
            neg_inf=neg_inf,
            H=h,
            N=n,
            DIM=d,
        )

    # Measure performance with per-iteration timing
    times_ms = []

    for _ in range(num_repeats):
        # Synchronize before measuring each iteration
        torch.cuda.synchronize()
        start = time.time()

        from trifast.triton import _bwd_b

        _bwd_b[b_grid](
            d_tensor,
            d_tensor.stride(0),
            d_tensor.stride(1),
            d_tensor.stride(2),
            q,
            q.stride(0),
            q.stride(1),
            q.stride(2),
            q.stride(3),
            k,
            k.stride(0),
            k.stride(1),
            k.stride(2),
            k.stride(3),
            v,
            v.stride(0),
            v.stride(1),
            v.stride(2),
            v.stride(3),
            bias,
            bias.stride(0),
            bias.stride(1),
            bias.stride(2),
            lse,
            lse.stride(0),
            lse.stride(1),
            lse.stride(2),
            mask,
            mask.stride(0),
            mask.stride(1),
            mask.stride(2),
            do,
            do.stride(0),
            do.stride(1),
            do.stride(2),
            do.stride(3),
            db,
            db.stride(0),
            db.stride(1),
            db.stride(2),
            sm_scale=sm_scale,
            neg_inf=neg_inf,
            H=h,
            N=n,
            DIM=d,
        )

        # Synchronize after each iteration to get accurate timing
        torch.cuda.synchronize()
        end = time.time()
        times_ms.append((end - start) * 1000)

    # Calculate statistics
    times_ms_array = np.array(times_ms)
    avg_time_ms = np.mean(times_ms_array)
    std_time_ms = np.std(times_ms_array)

    return {
        "kernel": "_bwd_b",
        "h": h,
        "n": n,
        "d": d,
        "avg_time_ms": float(avg_time_ms),
        "std_time_ms": float(std_time_ms),
        "min_time_ms": float(np.min(times_ms_array)),
        "max_time_ms": float(np.max(times_ms_array)),
        "iterations": num_repeats,
        "all_times_ms": times_ms,
    }


def run_all_profiles(
    h_values=[8],
    n_values=[128, 256],
    d_values=[64],
    device="cuda",
    dtype=torch.bfloat16,
    num_warmup=10,
    num_repeats=100,
):
    """
    Run profiling for all kernels with various parameters

    Args:
        h_values: List of head counts to test
        n_values: List of sequence lengths to test
        d_values: List of embedding dimensions to test
        device: Device to run on
        dtype: Data type for tensors
        num_warmup: Number of warmup iterations
        num_repeats: Number of iterations to measure

    Returns:
        List of profiling results
    """
    results = []

    for h in h_values:
        for n in n_values:
            for d in d_values:
                print(f"Profiling with h={h}, n={n}, d={d}")

                # Forward kernel
                fwd_result = profile_fwd_kernel(
                    h=h,
                    n=n,
                    d=d,
                    device=device,
                    dtype=dtype,
                    num_warmup=num_warmup,
                    num_repeats=num_repeats,
                )
                results.append(fwd_result)
                print(
                    f"  _fwd: {fwd_result['avg_time_ms']:.3f} ± {fwd_result['std_time_ms']:.3f} ms"
                )

                # Backward Q kernel
                bwd_q_result = profile_bwd_q_kernel(
                    h=h,
                    n=n,
                    d=d,
                    device=device,
                    dtype=dtype,
                    num_warmup=num_warmup,
                    num_repeats=num_repeats,
                )
                results.append(bwd_q_result)
                print(
                    f"  _bwd_q: {bwd_q_result['avg_time_ms']:.3f} ± {bwd_q_result['std_time_ms']:.3f} ms"
                )

                # Backward KV kernel
                bwd_kv_result = profile_bwd_kv_kernel(
                    h=h,
                    n=n,
                    d=d,
                    device=device,
                    dtype=dtype,
                    num_warmup=num_warmup,
                    num_repeats=num_repeats,
                )
                results.append(bwd_kv_result)
                print(
                    f"  _bwd_kv: {bwd_kv_result['avg_time_ms']:.3f} ± {bwd_kv_result['std_time_ms']:.3f} ms"
                )

                # Backward B kernel
                bwd_b_result = profile_bwd_b_kernel(
                    h=h,
                    n=n,
                    d=d,
                    device=device,
                    dtype=dtype,
                    num_warmup=num_warmup,
                    num_repeats=num_repeats,
                )
                results.append(bwd_b_result)
                print(
                    f"  _bwd_b: {bwd_b_result['avg_time_ms']:.3f} ± {bwd_b_result['std_time_ms']:.3f} ms"
                )

    return results


if __name__ == "__main__":
    # Example usage
    results = run_all_profiles(
        h_values=[4], n_values=[128, 256], d_values=[32], num_warmup=10, num_repeats=100
    )

    # Print summary
    print("\nSummary of results:")
    for result in results:
        print(
            f"{result['kernel']} (h={result['h']}, n={result['n']}, d={result['d']}): "
            + f"{result['avg_time_ms']:.3f} ± {result['std_time_ms']:.3f} ms "
            + f"[min: {result['min_time_ms']:.3f}, max: {result['max_time_ms']:.3f}]"
        )
