import time
import math
from config import *


M = None
  
def all_bin(m):
  """

  """
  M=[[1],[1,1]]
  for n in range(2,m+1): M.append([1]+[M[n-1][k-1]+M[n-1][k] for k in range(1,n)]+[1])
  return M  


def precompute():
  global M
  timeb=time.time()
  M=all_bin(MAX_PRECOMPUTED_COEFFS)
  print("binomials computed in time %.3f sec" %(time.time()-timeb)) 

  
def comb(n, k):
  """ Returns n choose k.
      If binomials coefficients were not precomputed yet, the table is filled before outputing.
      If n is too large to be in the precomputed table, math.comb() is used.
  """
  if M is None:
    precompute()

  if n < 0: 
    return 0
  elif n > MAX_PRECOMPUTED_COEFFS:
    return math.comb(n, k)
  else:
    try: 
      return M[n][k]
    except:
      print(n,k)
      raise
