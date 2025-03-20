import torch
from trifast.torch import triangle_attention, _triangle_attention
from trifast.utils import gen_tensors
from torch.library import opcheck
from torch.autograd import gradcheck


q, k, v, b, m = gen_tensors(16, 16, 1, True, "cuda", dtype=torch.bfloat16)

# q.requires_grad = False
# k.requires_grad = False
# v.requires_grad = False
# b.requires_grad = False
# m.requires_grad = False
#
# sm_scale = q.shape[-1] ** -0.5
# bs, h, _, n, dim = q.shape


for n in [16, 128, 256]:
    for d in [16, 32, 64]:
        for h in [1, 4]:
            q, k, v, b, m = gen_tensors(n, d, h, True, "cuda", dtype=torch.bfloat16)
            opcheck(_triangle_attention, (q, k, v, b, m), raise_exception=True)

# print(gradcheck(
#     _triangle_attention,
#     [q, k, v, b, m],
# ))
#

# o_a, l_a = fwd(q, k, v, b, m, sm_scale, bh, n, h, dim)
# print(o_a.isnan().any())
# print(l_a.isnan().any())
#
# o_b, l_b = torch.compile(fwd)(q, k, v, b, m, sm_scale, bh, n, h, dim)
#
# print(o_b.isnan().any())
# print(l_b.isnan().any())
#
# o_c, l_c = fwd(q, k, v, b, m, sm_scale, bh, n, h, dim)
#
# print((o_a - o_c).abs())
# print((l_a - l_c).abs())

# o_a = triangle_attention(q, k, v, b, m)
#
# o_b = triangle_attention(q, k, v, b, m)
#
# o_c = torch.compile(triangle_attention)(q, k, v, b, m)
#
# print((o_a - o_b).abs().max())
# print((o_a - o_c).abs().max())
