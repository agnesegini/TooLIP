import sys
sys.path.append('../tool/')

from printable import *



param_list = [ [ 40,  52, 104,  530,  80],
               [100,  24,  44,  982,  80],
               [ 65,  32,  63, 2560, 128], 
               [ 58,  35,  70, 4096, 128],
               [ 60,  35,  70, 8192, 128],
               [ 80, 260, 520, 1200, 128], 
               [ 70,  93, 186, 1499, 128], 
               [ 65,  96, 191, 1461, 128], 
               [ 70,  61, 122, 1777, 128], 
               [ 60,  98, 106, 2048, 128], 
               [160,  48,  96, 1987, 128]
             ]


print("Testing several parameters for XOR_TR")
res = []
for param_set in param_list:
  f = XOR_TR(param_set[:3])
  N = param_set[3]
  _lambda = param_set[4]
  res.append(tex_print_all(f, N, _lambda))

print("\n\n".join(res))
