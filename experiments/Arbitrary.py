import sys
sys.path.append('../tool/')


from printable import *
from header_functions import *

DEPTH=128


# Arbitrary 1
N=6000
n=450
AI=213

res = 0
nl = 2*sum([comb(n-2,i) for i in range(AI-2)])
p = [n, AI, res, nl]
G = BF_with(p)
F = D_SUM([G,XOR(256)])
tex_print_all(F,N,DEPTH)

# Arbitrary 2
N=2500
n=512
AI=256

res = 0
nl = 2*sum([comb(n-2,i) for i in range(AI-2)])
p = [n, AI, res, nl]
G = BF_with(p)
F = D_SUM([G,XOR(196)])
tex_print_all(F,N,DEPTH)

#Dahu
N=2500
n=512
AI=256

res = 255
nl = 2*sum([comb(n-2,i) for i in range(AI-2)])
p = [n, AI, res, nl]
G = BF_with(p)
tex_print_all(G,N,DEPTH)
