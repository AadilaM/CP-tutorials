# -*- coding: utf-8 -*-
"""
Created on Sat May  6 15:04:19 2017

@author: Aadila
"""

import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt

#Question 1

def shift(x,n=0):# x is array, n is shift constant
    vec=x*0#array of zeroes with same length as x
    assert vec.shape==x.shape
    vec[n]=1 #changing the nth element of vec to 1
    ftvec=fft(vec)
    ftx=fft(x)
    return np.real(ifft(ftx*ftvec))
    

x=np.arange(-10,10,0.1)
sigma=0.5
y=np.exp(-0.5*x**2/sigma**2)
yshift=shift(y,y.size/2)

plt.plot(x,yshift)
plt.ion()
plt.show()

#Question 2

def corr(a,b):
    assert a.size==b.size
    fta=fft(a)
    ftb=fft(b)
    conjftb=np.conj(ftb)
    return np.real(ifft(fta*conjftb))
    
#Use equation for Gaussian from above 

ycorr=corr(y,y)
plt.plot(x,ycorr)
plt.ion()
plt.show()


#Question 3

yshiftcorr=corr(yshift,yshift)

plt.plot(x,yshiftcorr,'r')
plt.plot(x,ycorr,'k')
plt.show()

print("It appears that the correlation of a function with itself is independent of shifting.")
print("This is expected, since the correlation is a measure of the statistical correlation between two functions and this would not change with shift.")

#Question 4

def convo_nowrap(c,d):
    assert c.size == d.size
    cnew=np.zeros(c.size*2)
    dnew=np.zeros(d.size*2)
    cnew[0:c.size]=c
    dnew[0:d.size]=d
    ft_cnew=fft(cnew)
    ft_dnew=fft(dnew)
    result=np.real(ifft(ft_cnew*ft_dnew))
    return result[0:c.size]

#Question 5

class Complex:
    def __init__(self, real=0, imag=0): #init gets called when new instance of Complex (object) is made
        self.r = real
        self.i = imag


    def __sub__(self, num): # subtraction between object itself and some other number
        return Complex(self.r - num.r,
                       self.i - num.i)

    def __mul__(self, num):
        return Complex(self.r*num.r - self.i*num.i,
                       self.i*num.r + self.r*num.i)

    def __div__(self, num):
        sr, si, orr, oi = self.r, self.i, num.r, num.i # introducing short forms
        r = float(orr**2 + oi**2)
        return Complex((sr*orr+si*oi)/r, (si*orr-sr*oi)/r)


#Testing

num1=Complex(2,4)
num2=Complex(1,2)

minus=num1.__sub__(num2)
print("num1 - num 2 = " +repr(minus.r) + "+i" +repr(minus.i))

quotient=num1.__div__(num2)
print("num1/ num 2 = " +repr(quotient.r) + "+i" +repr(quotient.i))

product= num1.__mul__(num2)
print("num1 *num 2 = " +repr(product.r) + "+i" +repr(product.i))
