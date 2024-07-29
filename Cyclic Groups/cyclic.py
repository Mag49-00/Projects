from math import floor

'''
Class for objects in the Cyclic groups

Variables:
int base:
    which cyclic group the object belongs to

int n:
    any number representation of the object

Methods:
value():
    returns the smallest non-negative number representation of the object

simplify():
    simplifies the object to its smallest non-negative representative

__str__():
    returns a string representation of the object of the form:
    "[B:n]", where B is the base of the cyclic group to which the object belongs,
    and n is its simplest non-negative integer representation

__repr__():
    identical to __str__

__eq__(Cyclic/int other):
    if other is Cyclic:
        returns true if the two are equivalent (have the same simplest representative), and false otherwise
        NOTE: if the other has a different base, raises an exception, as two cyclics of different bases are incomparable.
    if other is an int:
        creates a Cyclic of the same base as itself, with a number representation equal to the int
        then returns true if the two are equivalent, and false otherwise

__ne__(Cyclic/int other):
    returns the opposite of __eq__

__add__(Cyclic/int other):
    if other is Cyclic:
        returns the result of adding other to self, based on the addition operation in cyclic groups
        NOTE: if the other has a different base, raises an exception, as two cyclics of different bases are incomparable.
    if other is an int:
        converts it to a cyclic first, then adds the two

__radd__(Cyclic/int other):
    calculates the right addition to be consistent with __add__

__sub__(Cyclic/int other):
    if other is Cyclic:
        returns the result of subtracting other from self, based on the addition operation in cyclic groups
        NOTE: if the other has a different base, raises an exception, as two cyclics of different bases are incomparable.
    if other is an int:
        converts it to a cyclic first, then subtracts it

__rsub__(Cyclic/int other):
    calculates the right subtraction to be consistent with __sub__

__mul__(Cyclic/int other):
    if other is Cyclic:
        returns the multiplication of self and other, based on the multiplication operation in cyclic groups
        NOTE: if the other has a different base, raises an exception, as two cyclics of different bases are incomparable.
    if other is an int:
        converts it to a cyclic first, then multiplies

__rmul__(Cyclic/int other):
    calculates the right multiplication to be consistent with __mul__
    
__truediv__, __rtruediv__, __floordiv__, and __rfloordiv:
    calculate division or floor division between objects, but should not be used, as division is not usable in cyclic groups
    may still be used if intent is something more analagous to the 1-sphere -- in this case, all ints can also be floats (nothing
    explicitly in the code should break, theoretically)
'''
class Cyclic:
    def __init__(self,base,n):
        self.base=base
        self.n=n
        self.simplify()

    def value(self):
        return self.n%self.base

    def simplify(self):
        self.n=self.value()

    def __str__(self):
        self.simplify()
        return "["+str(self.base)+": "+str(self.n)+"]"

    def __repr__(self):
        return str(self)

    def __eq__(self,other):
        if other==None:
            return False
        if other.__class__.__name__=="Cyclic":
            return self.base==other.base and self.value()==other.value()
        return self==Cyclic(self.base,other)

    def __ne__(self,other):
        return (not self==other)

    def __add__(self,other):
        if other.__class__.__name__=="Cyclic":
            if self.base==other.base:
                return Cyclic(self.base,self.value()+other.value())
            raise Exception("Cannot add two cyclics of different bases.")
        return self+Cyclic(self.base,other)

    def __radd__(self,other):
        return self+other

    def __sub__(self,other):
        if other.__class__.__name__=="Cyclic":
            if self.base==other.base:
                return Cyclic(self.base,self.value()-other.value())
            raise Exception("Cannot add two cyclics of different bases.")
        return self-Cyclic(self.base,other)

    def __rsub__(self,other):
        return Cyclic(self.base,other)-self

    def __mul__(self,other):
        if other.__class__.__name__=="Cyclic":
            if self.base==other.base:
                return Cyclic(self.base,self.value()*other.value())
            raise Exception("Cannot add two cyclics of different bases.")
        return self*Cyclic(self.base,other)

    def __rmul__(self,other):
        return self*other

    def __truediv__(self,other):
        if other.__class__.__name__=="Cyclic":
            if self.base==other.base:
                return Cyclic(self.base,self.value()/other.value())
            raise Exception("Cannot add two cyclics of different bases.")
        return self/Cyclic(self.base,other)

    def __rtruediv__(self,other):
        return Cyclic(self.base,other)/self

    def __floordiv__(self,other):
        if other.__class__.__name__=="Cyclic":
            if self.base==other.base:
                return Cyclic(self.base,floor(self.value()/other.value()))
            raise Exception("Cannot add two cyclics of different bases.")
        return self/Cyclic(self.base,other)

    def __rfloordiv__(self,other):
        return Cyclic(self.base,other)//self
