# -*- coding: utf-8 -*-
"""
Created on Fri May 12 09:51:54 2017

@author: Aadila
"""

# Aadila Moola - Tut 3

import numpy as np
import matplotlib.pyplot as plt


#Problem 1 

class particle:
    def __init__(self, x=0, y=0, m=1.0,n=1000, G=1.0,soft=0.03):
        self.dict={}
        self.dict['n']=n
        self.dict['G']=G
f        self.dict['soft']=soft

        self.x=x 
        self.y=y 
        self.m=np.ones(self.dict['n'])*m
       
    def pot(self):
        potential=0
        for i in range(0,self.dict['n']):
            
            dx=self.x-self.x[i]
            dy=self.y-self.y[i]
            rsq=dx**2+dy**2
            soft=self.dict['soft']**2
            rsq[rsq<soft]=soft
            r=np.sqrt(rsq)
            potential+=self.dict['G']*np.sum((self.m*self.m[i])/r)
        return -0.5*potential #total potential between all particles 
 
#Problem 2

    def initialise (self):
        self.x=np.random.randn(self.dict['n'])#creating arrays of length n for the x and y values of n particles
        self.y=np.random.randn(self.dict['n'])#randn gives a sample from the normal distribution
        self.vx=np.zeros(self.dict['n'])
        self.vy=np.zeros(self.dict['n'])
        self.fx=np.zeros(self.dict['n'])
        self.fy=np.zeros(self.dict['n'])
     
    def force(self):
        for i in range(0,self.dict['n']):
            dx=self.x-self.x[i]
            dy=self.y-self.y[i]
            rsq=dx**2+dy**2
            soft=self.dict['soft']**2
            rsq[rsq<soft]=soft
            r=np.sqrt(rsq)
            r3=1.0/r*rsq
            self.fx[i]=-self.dict['G']*np.sum(self.m*dx*r3)
            self.fy[i]=-self.dict['G']*np.sum(self.m*dy*r3)  #This gives force/ m[i] (acceleration)
        return self.fx, self.fy 
        
        
   
    def evolve(self, tstep=0.1):
       
            self.x+=self.vx*tstep 
            self.y+=self.vy*tstep 
            
            potential=self.pot()
            
            self.vx+=self.fx*tstep
            self.vy+=self.fy*tstep
            
            kinetic=0.5*np.sum(self.m*(self.vx**2+self.vy**2) )
        
            return potential+ kinetic

n=1500
tstep=0.1
oversamp=5
part=particle(m=1.0/n)
part.initialise()

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-5, 5)) 
# 111 means: adding a 1x1 grid, in the first (only) subplot
line, = ax.plot([], [], '*', lw=2)
  

energy=np.array([])
def animate_points(crud):
    global system,line
    for i in range(oversamp):
        value=np.array(part.evolve())
    np.append(energy,value)
    print(value)
    line.set_data(part.x,part.y)

time=np.arange(0,tstep*energy.shape[0],tstep)
plt.plot(time,energy)

plt.show()


