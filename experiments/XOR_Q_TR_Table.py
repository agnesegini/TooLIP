import sys
sys.path.append('../tool/')

from printable import *



param_list = [[ 40, 10, 52, 104,  329,  80],
              [100, 10, 21,  44,  329,  80],
              [ 70, 10, 93, 186,  789, 128],
              [ 65, 10, 96, 191,  780, 128],
              [ 70, 10, 61, 122,  834, 128],
              [160, 10, 48,  96,  864, 128],
              [ 60, 20, 85, 170,  541, 128],
              [ 60, 20, 65, 150,  873, 128],
              [ 50, 40, 80, 160,  617, 128],
              [ 50, 60, 65, 150,  640, 128],
              [ 60, 40, 65, 150,  581, 128],
              [ 60, 60, 50, 100,  560, 128],
              [ 60, 60, 60, 120,  600, 128],
              [160, 15, 60, 120, 5000, 256],
              [140, 20, 60, 120, 4800, 256]
             ]


print("Testing several parameters for XOR_QUAD_TR")
res = []
for param_set in param_list:
  f = XOR_QUAD_TR(param_set[:4])
  N = param_set[4]
  _lambda = param_set[5]
  res.append(tex_print_all(f, N, _lambda))

print("\n\n".join(res))
