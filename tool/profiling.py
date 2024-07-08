from config import *
from header_functions import *

def accumulate_table(T, dimension=2):
  """ Accumulate probabilites in each row of the table in order to have Pr[X <= k] instead of Pr[X = k] at index k in the row.
      This extends naturally to dimension 3 by computing P[X <= k1 and Y <= k2] instead of Pr[(X,Y) = (k1, k2)] for each "layer".
  """
  if dimension == 2:
    for i in range(len(T)):
      for j in range(1, len(T[i])):
        T[i][j] += T[i][j-1]

  elif dimension == 3:
    for i in range(len(T)):
      accumulate_table(T[i])
      for j in range(1, len(T[i])):
        for k in range(len(T[i][j])):
          T[i][j][k] += T[i][j-1][k]

  return T

def profiling(F, DEPTH):
  """ Profiling phase of the algorithm.
      1. Create a profile table large enough to hold all possible values for each critetion at each level.
      2. For each level l:
        2.1 Compute the descendants of the function by fixing one more variable
        2.2 Evaluate the criteria on the descendants
        2.3 Update the profile with the new probability to obtain a given value for each criterion at level l
      3. Accumulate the table to get the probability of having the criterion <= to the index.

      Special case: DELTA_RES is a 3-dimensional table since it contains the probabilities for 2 criteria.
  """
  profile_AI = [[0 for _ in range(F.AI()+1)] for _ in range(DEPTH+1)]
  profile_AI[0][-1] = 1

  profile_EPS = [[0 for _ in range(SCALE_PRECISION_EPS//2 + 1)] for _ in range(DEPTH+1)]
  profile_EPS[0][F.EPS()] = 1

  profile_DELTA_RES = [[[0 for _ in range(F.max_res_descendants()+2)] for _ in range( SCALE_PRECISION_DELTA//2 + 1 )] for _ in range(DEPTH+1)] 
  profile_DELTA_RES[0][F.DELTA()][F.sRES()] = 1

  current_subf = {F: 1}

  for var_lambda in range(1, DEPTH+1):
      new_subf = {}

      for f, proba_parent in current_subf.items():
        for descendant, proba_descendant in f.descendants():
          new_subf[descendant] = new_subf.get(descendant, 0) + proba_parent*proba_descendant
      
      print('Depth:', var_lambda, '-- Nb descendants:', len(new_subf.keys())) 
      
      current_subf = new_subf # Parents can be forgotten once all descendants are computed.

      for f, proba in current_subf.items():
        profile_AI[var_lambda][f.AI()] += proba       
        profile_EPS[var_lambda][f.EPS()] += proba 
        profile_DELTA_RES[var_lambda][f.DELTA()][f.sRES()] += proba

  accumulate_table(profile_AI)
  accumulate_table(profile_DELTA_RES, 3)
  accumulate_table(profile_EPS)

  return profile_AI, profile_DELTA_RES, profile_EPS