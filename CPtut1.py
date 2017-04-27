# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 21:09:52 2017

@author: Aadila
"""
import math
import numpy as np
import matplotlib.pyplot as plt



#Problem 4- array slicing

r=np.arange(25)

#Taking all odd points
odd= r[1::2]

#Taking all even points excluding first and last points
even=r[2:2:-1]

#Problem 3-Area method

N=(10,30,100,300,1000)

alpha=[]
ErrA=[]
for n in N:
    x=np.linspace(0,np.pi/2,n) 
    y=np.cos(x)
    dx=np.pi/(2*n)
    Area=np.sum(y*dx)
    Error=abs(1.0-Area)
    ErrA.append(Error)
    a=math.log(Error,n)
    alpha.append(a)
    print("For n = "+ repr(n)+ " the area approximation is " +repr(Area)+" with error "+ repr(Error))


print("Area approx- Error scales with n like n to the power " + repr(np.average(alpha)))

#Problem 5-Simpson's Rule 

beta=[]
ErrS=[]
def Simpson(a,b,f,n):
    h=(b-a)/float(n)
    odd=0
    for i in range(1,n//2+1):
        odd+=(f(a+(2*i-1)*h))
    even=0
    for j in range(1,n//2):
        even+=(f(a+2*j*h))
    integral=(h/3)*(f(a)+4*(odd)+2*(even)+f(b))
    Err=abs(1.0-integral)
    ErrS.append(Err)
    b=math.log(Err,n)
    beta.append(b)
    print ("For n = "+repr(n)+" the Simpson's approximation is " +repr(integral)+" with error "+repr(Err))
        

         
def y(x):
    return np.cos(x)
    
for n in N:
    solution= Simpson(0,np.pi/2,y,n) 
    
print("Simpson's rule- Error scales with n like n to the power " + repr(np.average(beta)))

print("We need aproximately 14 points using the area method to match the level of accuracy of Simpson's method with 11 points")

#Problem 6- Plotting Error as a function of N

plt.plot(N,ErrA,'r',label='Area method')
plt.plot( N, ErrS, 'g',label="Simpon's method")
plt.xlabel("N")
plt.ylabel("Error")
plt.yscale('log')
plt.legend(loc='best')
plt.show()