from config import *
from math import log
from binomials import *

"""
available blocks:
  - XOR
  - TR
  - XOR_QUAD
  - QUAD
  - XOR_TR
  - XOR_TR_TR
  - XOR_QUAD_TR
  - multiTR
"""

class XOR:
  def __init__(self, internal_rep):
    self.k = internal_rep
    self.nb_var = self.k 

  def AI(self):
    return int(self.k>0) 
   
  def RES(self):
    return self.k-1
  
  def sRES(self):
    return self.RES()+1

  def NL(self):
    return 0

  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var))))

  def max_res_descendants(self):
    return self.RES()

  def descendants(self):
    den = 2*self.nb_var
    if self.k > 0:
      yield XOR(self.k - 1), 2*self.k/den
    
  def __eq__(self, other):
    return self.k == other.k

  def __hash__(self):
    return hash(self.k)

  def __repr__(self):
    return "({0})".format(self.k)

  def __str__(self):
    return "XOR_{0}".format(self.k)

    

class TR:
  def __init__(self, internal_rep):
    self.d = internal_rep[0]
    self.n = internal_rep[1]
    self.nb_var = self.n
    
    if self.d > (self.n+1)/2:
      self.d = self.n - self.d + 1

  def AI(self):
    return min(self.d, self.n-self.d+1)

  def RES(self):
    if self.n == 2*self.d - 1:
      return 0
    else:
      return -1

  def sRES(self):
    return self.RES()+1

  def NL_TR(d,n):
    if d == (n+1)/2:
      return 2**(n-1)- comb(n-1, (n-1)//2)
    elif d > (n+1)/2:
      s = 0
      for i in range(d, n+1):
        s += comb(n,i)
      return s
    elif d < (n+1)/2:
      s = 0
      for i in range(0, d):
        s += comb(n,i)
      return s
      
  def NL(self):
    return TR.NL_TR(self.d,self.n)
  
  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var))))

  def max_res_descendants(self):
    return self.RES()+1

  def descendants(self):
        den = 2*self.nb_var
        if self.n > 0:
          #Case 2 => set a variable in TR to 0
          if self.d > self.n:
            subf = TR([ self.n, self.n-1])
          else:
            subf = TR([self.d, self.n-1])
          yield subf, self.n/den

          #Case 3 => set a variable in TR to 1
          if self.d == 0:
            subf = TR([self.d, self.n-1])
          else:
            subf = TR([self.d-1, self.n-1])
          yield subf, self.n/den
    
  def __eq__(self, other):
    return (self.d, self.n) == (other.d, other.n)

  def __hash__(self):
    return hash(( self.d, self.n))

  def __repr__(self):
    return "({0}, {1})".format(self.d, self.n)

  def __str__(self):
    return "Tr({0},{1})".format(self.d, self.n)
    


class XOR_QUAD:
  def __init__(self, internal_rep):
    # [k, q, d, n, phantom]
    self.k = internal_rep[0]    
    self.q = internal_rep[1]

    if len(internal_rep) < 3:
      self.ph = 0
    else:
      self.ph = internal_rep[2]

    self.nb_var = self.k + 2*self.q + self.ph

  def AI(self):
    # lower bound on AI
    if self.q == 0:
      return int(self.k!=0)
    elif self.q == 1:
      return 1
    else:
      return 2
   
  def RES(self):
      return self.k-1

  def sRES(self):
    return self.RES()+1

  def NL(self):
    return 2**(2*self.q-1+self.k)-2**(self.q-1+self.k)
    
  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var-self.ph))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var-self.ph))))

  def max_res_descendants(self):
    return self.RES() + self.q 

  def descendants(self):
        den = 2*self.nb_var
        if self.k > 0:
          #Case 1 => set a XOR variable to 0 or 1
          yield XOR_QUAD([self.k - 1, self.q, self.ph]), 2*self.k/den

        if self.q > 0:
          #Case 2 => set a variable in QUAD to 0
          yield XOR_QUAD([self.k, self.q-1, self.ph+1]), 2*self.q/den
          
          #Case 3 => set a variable in QUAD to 1
          yield XOR_QUAD([self.k+1, self.q-1, self.ph]), 2*self.q/den

        if self.ph > 0:
          #Case 6 => set a phantom variable to 0 or 1
          yield XOR_QUAD([self.k, self.q, self.ph-1]), 2*self.ph/den

    
  def __eq__(self, other):
    return (self.k, self.q, self.ph) == (other.k, other.q, other.ph)

  def __hash__(self):
    return hash((self.k, self.q, self.ph))

  def __repr__(self):
    return "({0}, {1}, {2})".format(self.k, self.q,  self.ph)

  def __str__(self):
    return "XOR_{0} + QUAD_{1} and {2} spooky ghosts in {3} variables".format(self.k, self.q, self.ph, self.nb_var)   



class QUAD(XOR_QUAD):

  def __init__(self, internal_rep):
      XOR_QUAD.__init__(self, [0]+internal_rep)

  def __str__(self):
    return "QUAD_{0} and {1} spooky ghosts in {2} variables".format(self.q, self.ph, self.nb_var)
  


class XOR_TR:

  def __init__(self, internal_rep):
    self.k = internal_rep[0]
    self.d = internal_rep[1]
    self.n = internal_rep[2]
    self.nb_var = self.k + self.n
    
    if self.d > (self.n+1)/2:
      self.d = self.n - self.d + 1

  def AI(self):
    if self.d == (self.n+1)/2:
      return (self.n+1)//2
    elif (self.d == 0):
      if self.k == 0:
        return 0
      else:
        return 1
    elif (self.k == 0):
      return min(self.d, self.n-self.d+1)
    else:
      return min(self.d+1, self.n-self.d+2)  

  def RES(self):
    if self.n == 2*self.d - 1:
      return self.k
    else:
      return self.k-1

  def sRES(self):
    return self.RES()+1

  def NL(self):
    if self.d == (self.n+1)/2:
      return 2**(self.n+self.k-1) - (2**self.k)*comb(self.n-1, (self.n-1)//2)
    else:
      s = 0
      for i in range(0, self.d):
        s += comb(self.n,i)
      return (2**self.k)*s

  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var))))

  def max_res_descendants(self):
    return self.RES()+1

  def descendants(self):
        den = 2*self.nb_var
        if self.k > 1:
          #Case 1.a => set a XOR variable
          yield XOR_TR([self.k - 1, self.d, self.n]), 2*self.k/den
        elif self.k == 1:
          #Case 1.b => set a XOR when k is 1, the xor part vanishes.
          yield TR([self.d, self.n]), 2/den          

        if self.n > 0:
          #Case 2 => set a variable in TR to 0
          yield XOR_TR([self.k, self.d, self.n-1]), self.n/den

          #Case 3 => set a variable in TR to 1
          if self.d == 0:
            subf = XOR_TR([self.k, self.d, self.n-1])
          else:
            subf = XOR_TR([self.k, self.d-1, self.n-1])
          yield subf, self.n/den
    
  def __eq__(self, other):
    return (self.k, self.d, self.n) == (other.k, other.d, other.n)

  def __hash__(self):
    return hash((self.k, self.d, self.n))

  def __repr__(self):
    return "({0}, {1}, {2})".format(self.k, self.d, self.n)

  def __str__(self):
    return "XOR_{0} + Tr({1},{2})".format(self.k, self.d, self.n)
    return repr(self)
    
    
class XOR_TR_TR:

  def __init__(self, internal_rep):
    self.k = internal_rep[0]    
    self.d1 = internal_rep[1]
    self.n1 = internal_rep[2]
    self.d2 = internal_rep[3]
    self.n2 = internal_rep[4]
    
    if self.d1 > (self.n1+1)/2:
      self.d1 = self.n1 - self.d1 + 1

    if self.d2 > (self.n2+1)/2:
      self.d2 = self.n2 - self.d2 + 1
    
    if (self.n2,self.d2) < (self.n1,self.d1):
      self.d1, self.d2 = self.d2,self.d1
      self.n1, self.n2 = self.n2, self.n1
    self.nb_var = self.k + self.n1 + self.n2
    
  def AI(self):
    # lower bound on AI
    a = min(self.d1, self.n1 - self.d1+1)
    b = abs(self.n1 - 2*self.d1 + 1)
    c = min(self.d2, self.n2 - self.d2 + 1)+int(self.n2 != 2*self.d2-1)

    d = min(self.d2, self.n2 - self.d2+1)
    e = abs(self.n2 - 2*self.d2 + 1)
    f = min(self.d1, self.n1 - self.d1 + 1)+int(self.n1 != 2*self.d1-1)

    return max((a+min(b,c)), (d+min(e,f)))
   
  def RES(self):
    if (self.n1 == 2*self.d1 - 1) and (self.n2 == 2*self.d2 - 1):
      return self.k+1
    elif (self.n1 != 2*self.d1 - 1) and (self.n2 != 2*self.d2 - 1):
      return self.k-1
    else:
      return self.k

  def sRES(self):
    return self.RES()+1

  def NL(self):
    NL_XTr1 = XOR_TR([self.k, self.d1, self.n1]).NL()
    NL_Tr2  = XOR_TR([0, self.d2, self.n2]).NL()

    return (2**(self.n2))*NL_XTr1 + (2**(self.k+self.n1))*NL_Tr2 - 2*NL_XTr1*NL_Tr2

  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var))))

  def max_res_descendants(self):
    return self.RES() + 2

  def descendants(self):
        den = 2*self.nb_var
        if self.k > 0:
          #Case 1 => set a XOR variable to 0
          yield XOR_TR_TR([self.k - 1, self.d1, self.n1,self.d2, self.n2]), 2*self.k/den

        if self.n1 > 0:
          #Case 2 => set a variable in TR to 0
          if self.d1 > self.n1:
            subf = XOR_TR_TR([self.k, self.n1, self.n1-1, self.d2, self.n2])
          else:
            subf = XOR_TR_TR([self.k, self.d1, self.n1-1, self.d2, self.n2])
          yield subf, self.n1/den

          #Case 3 => set a variable in TR to 1
          if self.d1 == 0:
            subf = XOR_TR_TR([self.k, self.d1, self.n1-1, self.d2, self.n2])
          else:
            subf = XOR_TR_TR([self.k, self.d1-1, self.n1-1, self.d2, self.n2])
          yield subf, self.n1/den
          
        if self.n2 > 0:
          #Case 4 => set a variable in 2ndTR to 0
          if self.d2 > self.n2:
            subf = XOR_TR_TR([self.k, self.d1, self.n1, self.n2, self.n2-1])
          else:
            subf = XOR_TR_TR([self.k, self.d1, self.n1, self.d2, self.n2-1])
          yield subf, self.n2/den

          #Case 5 => set a variable in 2ndTR to 1
          if self.d2 == 0:
            subf = XOR_TR_TR([self.k, self.d1, self.n1, self.d2, self.n2-1])
          else:
            subf = XOR_TR_TR([self.k, self.d1, self.n1, self.d2-1, self.n2-1])
          yield subf, self.n2/den
          
    
  def __eq__(self, other):
    return (self.k, self.d1, self.n1, self.d2, self.n2) == (other.k, other.d1, other.n1, other.d2, other.n2)

  def __hash__(self):
    return hash((self.k, self.d1, self.n1, self.d2, self.n2))

  def __repr__(self):
    return "({0}, {1}, {2}, {3}, {4})".format(self.k, self.d1, self.n1, self.d2, self.n2)

  def __str__(self):
    return "XOR_{0} + Tr({1},{2}) + Tr({3},{4})".format(self.k, self.d1, self.n1, self.d2, self.n2)



class XOR_QUAD_TR:

  def __init__(self, internal_rep):
    # [k, q, d, n, phantom]
    self.k = internal_rep[0]    
    self.q = internal_rep[1]
    self.d = internal_rep[2]
    self.n = internal_rep[3]

    if len(internal_rep) < 5:
      self.ph = 0
    else:
      self.ph = internal_rep[4]

    self.nb_var = self.k + 2*self.q + self.n + self.ph
    
    if self.d > (self.n+1)/2:
      self.d = self.n - self.d + 1



  def AI(self):
    # lower bound on AI
    if (self.n - 2*self.d + 1) == 0:
      return (self.n+1)//2
    elif abs(self.n - 2*self.d + 1) == 1:
      return min(self.d+1, self.n - self.d + 2)
    else:
      return min(self.d+2, self.n - self.d + 3)
   
  def RES(self):
    if self.n == 2*self.d - 1:
      return self.k
    else:
      return self.k-1

  def sRES(self):
    return self.RES()+1

  def NL(self):
    NL_XTr = XOR_TR([self.k, self.d, self.n]).NL()
    
    s1 = (2**(self.k+self.n)) * (2**(2*self.q-1) - 2**(self.q-1))
    s2 = (2**(self.q))*NL_XTr
    
    return s1 + s2

  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var-self.ph))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var-self.ph))))

  def max_res_descendants(self):
    return self.RES() + self.q + 1


  def descendants(self):
    den = 2*self.nb_var
    if self.k > 0:
      #Case 1 => set a XOR variable to 0 or 1
      yield XOR_QUAD_TR([self.k - 1, self.q, self.d,self.n, self.ph]), 2*self.k/den

      
    if self.q > 0:
      #Case 2 => set a variable in QUAD to 0
      yield XOR_QUAD_TR([self.k, self.q-1, self.d, self.n, self.ph+1]), 2*self.q/den
      
      #Case 3 => set a variable in QUAD to 1
      yield XOR_QUAD_TR([self.k+1, self.q-1, self.d, self.n, self.ph]), 2*self.q/den

      
    if self.n > 0:
      #Case 4 => set a variable in TR to 0
      if self.d > self.n:
        subf = XOR_QUAD_TR([self.k, self.q, self.n, self.n-1, self.ph])
      else:
        subf = XOR_QUAD_TR([self.k, self.q, self.d, self.n-1, self.ph])
      yield subf, self.n/den

      #Case 5 => set a variable in TR to 1
      if self.d == 0:
        subf = XOR_QUAD_TR([self.k, self.q, self.d, self.n-1, self.ph])
      else:
        subf = XOR_QUAD_TR([self.k, self.q, self.d-1, self.n-1, self.ph])
      yield subf, self.n/den

    if self.ph > 0:
      #Case 6 => set a phantom variable to 0 or 1
      yield XOR_QUAD_TR([self.k, self.q, self.d,self.n, self.ph-1]), 2*self.ph/den

    
  def __eq__(self, other):
    return (self.k, self.q, self.d, self.n, self.ph) == (other.k, other.q, other.d, other.n, other.ph)

  def __hash__(self):
    return hash((self.k, self.q, self.d, self.n, self.ph))

  def __repr__(self):
    return "({0}, {1}, {2}, {3}, {4})".format(self.k, self.q, self.d, self.n, self.ph)

  def __str__(self):
    return "XOR_{0} + QUAD_{1} + Tr({2},{3}) and {4} spooky ghosts in {5} variables".format(self.k, self.q, self.d, self.n, self.ph, self.nb_var)



class multiTR:

  def can_rep(d,n):
    if d > (n+1)/2:
      d = n - d + 1

    return (d,n)

  def __init__(self, internal_rep):  # We want pairs
    self.pairs = [multiTR.can_rep(*internal_rep[i]) for i in range(len(internal_rep))]
    (self.pairs).sort()
    self.nb_var = sum([p[1] for p in self.pairs])
    self.nb_tr = len(self.pairs)
    
  def AI(self):
    return max([min(d, n-d+1) for (d,n) in self.pairs])
   
  def RES(self):
    return sum([-int(n != 2*d - 1) for (d,n) in self.pairs])+self.nb_tr-1

  def sRES(self):
    return self.RES()+1

  def NL(self):
    NL_f = TR.NL_TR(*(self.pairs[0]))
    n = self.pairs[0][1]

    for next_function in self.pairs[1:]:
      NL_g = TR.NL_TR(*next_function)
      m = next_function[1]
      
      NL_f = (1<<m)*NL_f + (1<<n)*(NL_g) - 2*(NL_f)*(NL_g)
      n += m

    return NL_f

  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var))))

  def max_res_descendants(self):
    return self.RES() + self.nb_tr

  def descendants(self):
    den = 2*self.nb_var
    for i in range(len(self.pairs)):
       f = TR(list(self.pairs[i]))
       for d, proba in f.descendants():
          yield multiTR(self.pairs[:i] + [(d.d, d.n)] + self.pairs[i+1:]), proba*(2*f.nb_var)/den  
          
    
  def __eq__(self, other):
    return self.pairs == other.pairs

  def __hash__(self):
    return hash(str(self.pairs))

  def __repr__(self):
    return str(self.pairs)

  def __str__(self):
    s = ""
    for tr in self.pairs[:-1]:
      s += "Tr({0},{1}) + ".format(tr[0], tr[1])

    s += "Tr({0},{1})".format(self.pairs[-1][0], self.pairs[-1][1])
    return s
 


class BF_with:
  def __init__(self, params): #[nvar,AI,res,nl]
    self.nb_var = params[0]
    self.ai=max(0,params[1])
    self.res=max(-1,params[2])
    self.nl=params[3]
    self.params=[self.nb_var,self.ai,self.res,self.nl]
    
  def AI(self):
    return self.ai

  def RES(self):
    return self.res

  def sRES(self):
    return self.RES()+1

  def NL(self):
      return self.nl

  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var))))

  def max_res_descendants(self):
    return self.res


  def descendants(self):
        
    nl= 2*sum([comb(self.nb_var-2,i) for i in range(self.ai-2)])
    yield BF_with([self.nb_var-1, self.ai-1, self.res-1, nl ] ) , 1
 
  def __eq__(self, other):
    return self.params == other.params

  def __hash__(self):
    return hash(str(self.params))

  def __repr__(self):
    return "({0})".format(self.params)

  def __str__(self):
     return "Boolean function in {0} variable with AI {1}, resiliency {2} and nonlinearity {3}".format(*self.params)

