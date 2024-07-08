from config import *

class D_SUM:
  def __init__(self, sub_functions):
    self.nb_var = 0
    self.sub_functions = sub_functions
    for f in self.sub_functions:
      self.nb_var += f.nb_var

  def AI(self):
    return max(f.AI() for f in self.sub_functions)

  def RES(self):
    return sum(f.RES() for f in self.sub_functions) + len(self.sub_functions) - 1

  def sRES(self):
    return self.RES()+1

  def NL(self):
    NL_f = self.sub_functions[0].NL()
    n = self.sub_functions[0].nb_var

    for next_function in self.sub_functions[1:]:
      NL_g = next_function.NL()
      m = next_function.nb_var
      
      NL_f = (1<<m)*NL_f + (1<<n)*(NL_g) - 2*(NL_f)*(NL_g)
      n += m

    return NL_f

  def EPS(self):
    return int(SCALE_PRECISION_EPS*(self.NL()/(2**(self.nb_var))))

  def DELTA(self):
    return int(SCALE_PRECISION_DELTA*(self.NL()/(2**(self.nb_var))))

  def max_res_descendants(self):
    return sum(f.max_res_descendants() for f in self.sub_functions) + len(self.sub_functions) - 1

  def descendants(self):
        den = 2*self.nb_var

        for i in range(len(self.sub_functions)):
          f = self.sub_functions[i]
          for d, proba in f.descendants():
            yield D_SUM(self.sub_functions[:i] + [d] + self.sub_functions[i+1:]), proba*(2*f.nb_var)/den   

 
  def __eq__(self, other):
    return self.sub_functions == other.sub_functions

  def __hash__(self):
    return hash(str(self.sub_functions))

  def __repr__(self):
    return "({0})".format(self.sub_functions)

  def __str__(self):
    s = ""
    for f in self.sub_functions[:-1]:
      s += str(f) +  " + "
    s += str(self.sub_functions[-1])
    return s
