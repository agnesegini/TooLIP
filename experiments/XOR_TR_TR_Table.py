import sys
sys.path.append('../tool/')

from printable import *



param_list = [[ 40, 26, 52, 26, 52,  360,  80],
              [100, 11, 22, 11, 22,  397,  80],
              [ 54, 19, 38, 19, 38, 6500, 128],
              [ 54, 22, 45, 23, 45, 3072, 128],
              [ 65, 47, 95, 48, 96,  830, 128],
              [ 70, 30, 61, 31, 61,  841, 128],
              [160, 24, 48, 24, 48,  913, 128],
              [ 70, 46, 93, 47, 93,  736, 128],
              [ 60, 26, 53, 27, 53, 1229, 128]
             ]


print("Testing several parameters for XOR_TR_TR")
res = []
for param_set in param_list:
  f = XOR_TR_TR(param_set[:5])
  N = param_set[5]
  _lambda = param_set[6]
  res.append(tex_print_all(f, N, _lambda))

print("\n\n".join(res))
