class BOOLEAN_FUNCTION:
  """This class is an empty template showing the interface used by the profiling code.
     It can be used as a starting point to evaluate the attacks on new functions.
     All the methods except repr and str are mandatory to evaluate the complexities.
     We encourage to look at a concrete instanciation (like XOR_TR) in the function module while reading this template. 
  """


  def __init__(self, internal_rep):
    """ The internal representation is arbitrary and decided by the implementer but should identify unambiguously the function.
    """


    self.nb_var = None 
    pass

  def AI(self):
    pass 
   
  def RES(self):
    pass
  
  def sRES(self):
    """ Since resiliency can be -1, we shift it by one in practice to get a positive integer.
        This is convenient because we want to use it as an index in the profile table.
    """
    return self.RES()+1

  def NL(self):
    pass

  def EPS(self):
    """ The value is supposed to be a real number in the range [0, 0.5].
        To handle this, we discretize the interval using a fixed point representation with denominator SCALE_PRECISION_EPS.
        E.g. if SCALE_PRECISION_EPS = 100, the function returns a value between 0 and 500.
    """
    pass

  def DELTA(self):
    """ Same as EPS except that the denominator is SCALE_PRECISION_DELTA.
    """
    pass

  def max_res_descendants(self):
    """ This function should return the maximum resiliency among all descendants of the function.
        This is needed to know the size of the profile table. 
        Technically, we can stop at descendants up to a given depth (equal to the security parameter) because the others will not be explored.
    """
    pass

  def descendants(self):
    """ This function is a generator yielding the direct descendants (obtained by fixing one variable) of the function as well as their probability
        For example if the function has only two descendants of equal probability when fixing a variable, the body of this method would look like:

          yield BOOLEAN_FUNCTION(XXX), 0.5
          yield BOOLEAN_FUNCTION(YYY), 0.5
        
        where XXX (resp. YYY) defines the function obtained when setting a variable to 0 (resp. 1).
        Note that the function object yield can be from a different class (implementing a function) in case fixing a variable simplifies the function. 
    """
    pass
    
  def __eq__(self, other):
    pass

  def __hash__(self):
    """ Since descendants are stored as keys in a dictionnary, hash should be defined.
        Simplest way is to hash the internal representation.
    """
    pass

  def __repr__(self):
    pass

  def __str__(self):
    pass
