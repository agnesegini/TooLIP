from math import  log
from config import *
from binomials import *


class AI_attack:
  def __init__(self, profile, F, N):
    self.profile = profile
    self.F = F
    self.N = N
    self.cx,self.L="run method complexity!","run method complexity!"
    self.NAME ='AI'
  
  def D(self,k,n):
    s = 0
    for i in range(k+1):
      s+= comb(n, i)
    return s
  
  def data(self, k, n):
    return log(self.D(k, n)/(comb(n, k)),2)
  def time(self, k, n):
    return OMEGA*log(self.D(k, n),2)

  def complexity(self):
    MAX_DEPTH = len(self.profile)
    MAX_AI = len(self.profile[0])-1
    NUM_VAR_F = self.F.nb_var;
    best_complexity = 1000
    best_L=-1
    count = 0
    
    for L in range(0, MAX_DEPTH):
      k = 0
      while k <= MAX_AI:
        time_complexity = L+self.time(k, self.N-L)

        if time_complexity > best_complexity:
          k = MAX_AI+1
        else:
          proba = 0
          for ell in range(L+1):
            proba_L_ell = comb(L, ell)*comb(self.N-L, NUM_VAR_F - ell)/comb(self.N, NUM_VAR_F)
            proba += proba_L_ell*self.profile[ell][k]
          if proba != 0:
            data_complexity = self.data(k, self.N-L)-log(proba,2)
            complexity = max(time_complexity,DATA_SCALE*data_complexity)
            if complexity < best_complexity:
              best_complexity = complexity
              best_L=L
          else:
            count += 1
              
        
        k += 1
    self.cx,self.L=best_complexity,best_L

class FAI_attack:
  def __init__(self, profile, F, N):
    self.profile = profile
    self.F = F
    self.N = N
    self.cx,self.L="run method complexity!","run method complexity!"
    self.NAME ='FAI'
  
  def D(self,k,n):
    s = 0
    for i in range(k+1):
      s+= comb(n, i)
    return s
  
  def data(self, k, n):
    return log(self.D(k, n)/(comb(n, k)),2)

  def time(self, k, n):
    val_D = self.D(k, n)
    return log(val_D*log(val_D,2)*log(val_D,2) + (n+1) * val_D*log(val_D,2) + (n+1)**OMEGA,2)

  def complexity(self):
    MAX_DEPTH = len(self.profile)
    MAX_AI = len(self.profile[0])-1
    NUM_VAR_F = self.F.nb_var;
    best_complexity = 1000
    best_L=-1
    self.best_k = -1
    
    for L in range(0, MAX_DEPTH):
      k = 0
      while k <= MAX_AI:
        time_complexity = L+self.time(k, self.N-L)
        if time_complexity > best_complexity:
          k = MAX_AI+1
        else:
          proba = 0
          for ell in range(L+1):
            proba_L_ell = comb(L, ell)*comb(self.N-L, NUM_VAR_F - ell)/comb(self.N, NUM_VAR_F)
            proba += proba_L_ell*self.profile[ell][k]

          if proba != 0:
            data_complexity = self.data(k, self.N-L)-log(proba,2)
            complexity = max(time_complexity, DATA_SCALE*data_complexity)
            if complexity < best_complexity:
              best_complexity = complexity
              best_L=L
              self.best_k = k
        
        k += 1
    self.cx,self.L=best_complexity,best_L
  


class DELTA_RES_attack:
  def __init__(self, profile, F, N):
    self.profile = profile
    self.F = F
    self.N = N
    self.cx,self.L="run method complexity!","run method complexity!"
    self.NAME ='DELTA_RES'
    
  def data(self, delta, res):
    if delta == 0:
      return 256
    return res - 2*log(delta, 2)

  def time(self, delta):
    if delta == 0:
      return 256
    return - 2*log(delta, 2)

  def complexity(self):
    MAX_DEPTH = len(self.profile)
    MAX_DELTA = SCALE_PRECISION_DELTA//2
    MAX_RES = len(self.profile[0][0])
    NUM_VAR_F = self.F.nb_var;
    best_complexity = 256
    best_L=-1
   
    for L in range(0, MAX_DEPTH):
      delta = 0

      while delta <= MAX_DELTA:
        time_complexity = L+self.time(0.5-delta/SCALE_PRECISION_DELTA)
        if time_complexity > best_complexity:
          delta = MAX_DELTA+1
        else:
          for res in range(MAX_RES):
            proba = 0
            for ell in range(L+1):
              proba_L_ell = comb(L, ell)*comb(self.N-L, NUM_VAR_F - ell)/comb(self.N, NUM_VAR_F)
              proba += proba_L_ell*self.profile[ell][delta][res]

            if proba != 0:
              data_complexity = self.data(0.5-delta/SCALE_PRECISION_DELTA, res-1)-log(proba,2) #we accumulate res+1!
              complexity = max(time_complexity, DATA_SCALE*data_complexity)
              if complexity < best_complexity:
                best_complexity = complexity
                best_L=L
        
        delta += 1
    self.cx,self.L=best_complexity,best_L    



class EPS_attack:
  def __init__(self, profile, F, N):
    self.profile = profile
    self.F = F
    self.N = N
    self.cx,self.L="run method complexity!","run method complexity!"
    self.NAME ='EPS'
    
  def data(self, n):
    return log(n,2)

  def time(self, eps, n):
    return OMEGA*log(n,2) - n*log(1-eps,2)
 


  def complexity(self):
    MAX_DEPTH = len(self.profile)
    NUM_VAR_F = self.F.nb_var;
    best_complexity = 256
    best_L=-1
    
    for L in range(0, MAX_DEPTH):
      eps = 0
      while eps <= SCALE_PRECISION_EPS//2:
        time_complexity = L+self.time(eps/SCALE_PRECISION_EPS, self.N)
        if time_complexity > best_complexity:
          eps = SCALE_PRECISION_EPS//2+1
        else:
        
          proba = 0
          for ell in range(L+1):
            proba_L_ell = comb(L, ell)*comb(self.N-L, NUM_VAR_F - ell)/comb(self.N, NUM_VAR_F)
            proba += proba_L_ell*self.profile[ell][eps]

          if proba != 0:
            data_complexity = self.data(self.N-L)-log(proba,2)
            complexity = max(time_complexity, DATA_SCALE*data_complexity)
            if complexity < best_complexity:
              best_complexity = complexity
              best_L=L
        
        eps += 1
    self.cx,self.L=best_complexity,best_L


  
