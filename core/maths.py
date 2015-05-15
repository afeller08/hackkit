from collections import Iterable
from numbers import Number
import math
from hackkit.helpers.slightly import Inferred

class Vector(tuple):
    def __new__(self, iterable, *args):
        if isinstance(iterable, Iterable) and len(args) == 0:
            return super(Vector, self).__new__(self, iterable)
        else:
            iterable = [iterable] + list(args)
            return super(Vector,self).__new__(self, iterable)

    def __init__(self, iterable, *args):
        if isinstance(iterable, Iterable) and len(args) == 0:
            super(Vector, self).__init__(self, iterable)
        else:
            iterable = [iterable] + list(args)
            super(Vector, self).__init__(self, iterable)

    def __add__(self, other):
        v = [x + y for x,y in zip(self,other)]
        return self.__class__(v)

    def __mul__(self, other):
        if isinstance(other, Number):
            v = [other * x for x in self]
            return self.__class__(v)
        else:
            return sum([x * y for x,y in zip(self,other)])

class _RenormalizedFloat:
    __metaclass__ = Inferred

class _RFmc(Inferred, Number.__metaclass__):
    pass

class RenormalizedFloat(_RenormalizedFloat, Number):
    ''' Renormalized floats are to floats as longs are to ints.
        It's less pure than Decimal. If you're using Decimals because you don't
        want the kind of rounding floats have, this is more like a float.

        If you want something that behaves like a float but can handle numbers
        bigger than 10 ** 308 or smaller than 10 ** -335. And uses a relaxed
        definition of equality.
        
        Use case: you are prototyping code dealing with probability, using
        floats, and you have to deal with numbers that are too small for
        your code to be able to handle, and you don't want to go through
        all of your code and cast every float to a Decimal just to text your
        approach to see if it works.
    '''
    __metaclass__ = _RFmc

    def __init__(self, number=0, exp=None):
        if exp is None:
            self.exp = int(math.floor(math.log10(number)))
            self.val = number * 10 ** -self.exp
        else:
            self.val = number
            self.exp = exp
    
    def __float__(self):
        return self.val * 10 ** self.exp

    def __int__(self):
        return int(self.val * 10 ** self.exp)
    
    def __repr__(self):
        return '{0}e{1}'.format(self.val, self.exp)

    def __mul__(self, other):
        if not isinstance(other, Number):
            return NotImplemented
        if not isinstance(other, RenormalizedFloat):
            other = RenormalizedFloat(other)
        exp = self.exp + other.exp
        val = self.val + other.val
        if val > 10:
            val /= 10.0
            exp += 1
        return self.__class__(val, exp)

    def __add__(self, other):
        if not isinstance(other, Number):
            return NotImplemented
        if not isinstance(other, RenormalizedFloat):
            other = RenormalizedFloat(other)
        if self.exp < other.exp:
            self.val *= 10 ** (self.exp - other.exp)
            return self.__class__(self.val - other.val, other.exp)

    def __eq__(self, other):
        if not isinstance(other, Number):
            return NotImplemented
        if not isinstance(other, RenormalizedFloat):
            other = RenormalizedFloat(other)
        if self.exp == other.exp and abs(self.val - other.val) < 10 ** -13:
            return True
        else:
            return False
