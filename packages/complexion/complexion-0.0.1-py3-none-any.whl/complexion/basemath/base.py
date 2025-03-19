from sympy import (sin as SIN,tan as TAN,cos as COS,asin as ASIN,atan as ATAN,acos as ACOS,
                sinh as SINH,tanh as TANH,cosh as COSH,acosh as ACOSH,asinh as ASINH,atanh as ATANH,
                   exp as EXP,sqrt as SQRT,cbrt as CBRT,root as ROOT,csc as CSC,pi
                    )
from math import e
__all__ = []
def sim(x):
    if type(x)==complex:
        a=x.real
        b=x.imag
        return complex(a,b)
    return float(x)
def sin(x):return sim(SIN(x))
def tan(x):return sim(TAN(x))
def cos(x):return sim(COS(x))
def asin(x):return sim(ASIN(x))
def atan(x):return sim(ATAN(x))
def acos(x):return sim(ACOS(x))
def sinh(x):return sim(SINH(x))
def cosh(x):return sim(COSH(x))
def tanh(x):return sim(TANH(x))
def asinh(x):return sim(ASINH(x))
def acosh(x):return sim(ACOSH(x))
def atanh(x):return sim(ATANH(x))
def exp(x):return sim(EXP(x))
def sqrt(x):return sim(SQRT(x))
def cbrt(x):return sim(CBRT(x))
def root(x,y):return sim(ROOT(x,y))
def csc(x):return sim(CSC(x))
pi=sim(pi)
e=sim(e)
