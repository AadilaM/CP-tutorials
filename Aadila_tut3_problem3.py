# -*- coding: utf-8 -*-
"""
Tut3 -Problem 3

Created on Mon May 15 20:49:03 2017

@author: Aadila
"""

import numpy as np
import matplotlib.pyplot as plt

npoints=100
order=10
d=np.random.randn(npoints) #generating random data
x=np.arange(0,npoints+1)

xvar=np.arange(0,npoints)/2*np.pi*npoints
a=np.zeros([npoints,2*order-1])
a[:,0]=1
for i in range (1,order):
    a[:,2*i-1]=np.cos(i*xvar)
    a[:,2*i]=-np.sin(i*xvar)

    
aa=np.matrix(a)
dd=np.matrix(d).transpose()
lhs=aa.transpose()*dd
rhs=aa.transpose()*aa
m=np.linalg.inv(rhs)*lhs
mu=aa*m

