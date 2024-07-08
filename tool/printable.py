### To print in a file call python3 printable.py > namefile.txt 

from attacks import *
from header_functions import *
from profiling import *

def tex_print_att(F,N,DEPTH,attack,profile=None):
  print(attack)
  print(F, N, DEPTH,  sep=' ~&~ ', end=' ~&~ ')
  if not profile: pAI, pRES, pEPS = profiling(F,DEPTH) 
  if attack=='AI': A=AI_attack(pAI, F, N)
  elif attack=='FAI': A=FAI_attack(pAI, F, N)
  elif attack=='DEL': A=DELTA_RES_attack(pRES, F, N)
  elif attack=='EP': A=EPS_attack(pEPS, F, N)
  else: raise Exception("No valid attack.")
  A.complexity()
  print(A.cx, A.L, sep=' ~&~ ', end=' ~\\\\')
  print('\n')
  
def tex_print_all(F,N,DEPTH, verbose=True):
  s = "N: " + str(N) + " lambda: " + str(DEPTH) + "\n" + str(F) +"\n"
  if verbose: print(s)
  pAI, pRES, pEPS = profiling(F,DEPTH)
  A1 = AI_attack(pAI, F, N)
  A2 = FAI_attack(pAI, F, N)
  A3 = DELTA_RES_attack(pRES, F, N)
  A4 = EPS_attack(pEPS, F, N)
  for A in [A1, A2, A3, A4]:
    A.complexity()
    if verbose: print(A.NAME, "%.5f" %A.cx, A.L, sep=' ~&~ ', end=' ~\\\\\n')
    s += A.NAME + " %.5f ~&~ "%A.cx + " ~&~ " + str(A.L) + "~\\\\\n"
  return s

