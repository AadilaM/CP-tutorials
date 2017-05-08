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
    def __init__ (self,r=0,i=0):
        self.r=r
        self.i=i
    
    def copy(self):
        return Complex(self.r, self.i)
        
        
    def __sub__(self,num ):
        sol=self.copy()
        sol.r -= num.r
        sol.i-=num.i
        return sol
        
    def __mul__(self,num):
        sol=self.copy()
        prodr=0
        prodi=0
        
        prodr+=sol.r*num.r
        prodi+=sol.i*num.i
        prodr+=num.r*sol.r
        prodi+=sol.i*num.i

        sol.r=prodr
        sol,i=prodi

        return sol

    def __div__(self,num):
        sol=self.copy()
        conjnum=Complex(num.r,num.i*-1)
        a=sol.__mul__(conjnum)
        b=num.__mul__(conjnum)

        sol.r=a.r/b.r
        sol.i= a.i/b.i
        return sol
        
#Testing

num1=Complex(2,4)
num2=Complex(1,2)

minus=num1 -num2
print("num1 - num 2 = " +repr(minus.r) + "+i" +repr(minus.i))

quotient=num1/num2
print("num1/ num 2 = " +repr(quotient.r) + "+i" +repr(quotient.i))

product= num1*num2
print("num1 *num 2 = " +repr(product.r) + "+i" +repr(product.i))
