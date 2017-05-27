# -*- coding: utf-8 -*-
"""
Created on Mon May 15 23:57:15 2017

@author: Aadila
"""

import numpy as np

def sim_lorentzian(t,a=1,b=1,c=0): #should we add offset, amp etc?
    dat=a/(b+(t-c)**2)
    dat+=np.random.randn(t.size)
    return dat
    


#class Lorentzian:
#    def __init__(self, t,a=1,b=1,c=0):
#      self.t=t
#      self.y=sim_lorentzian(t,a,b,c)
#      self.err=np.ones(t.size) #error in measurement of noisy data?
#      self.a=a
#      self.b=b
#      self.c=c

class Lorentzian:
    def __init__(self, t,a=1,b=0.5,c=0,offset=0): #a=amp, c=cent
      self.t=t
      self.y=sim_lorentzian(t,a,b,c)+offset
      self.err=np.ones(t.size) #error in measurement of noisy data?
      self.a=a
      self.b=b
      self.c=c
      
      
    def get_chisq(self,vec):
        a=vec[0]
        b=vec[1]
        c=vec[2]
        offset=vec[3]
        

        pred= offset+ a/(b+(self.t-c)**2) #predicted values of lorentzian
        chisq=np.sum(  (self.y-pred)**2/self.err**2) #chi-squared
        return chisq
        
        
def get_trial_offset(sigs):
    return sigs*np.random.randn(sigs.size)
      

        
def run_mcmc(data,start_pos,nstep,scale=None):
    nparam=start_pos.size
    params=np.zeros([nstep,nparam+1])
    params[0,0:-1]=start_pos
    cur_chisq=data.get_chisq(start_pos)
    cur_pos=start_pos.copy()
    if scale==None:
        scale=np.ones(nparam)
    for i in range(1,nstep):
        new_pos=cur_pos+get_trial_offset(scale)
        new_chisq=data.get_chisq(new_pos)
        if new_chisq<cur_chisq:
            accept=True
        else:
            delt=new_chisq-cur_chisq
            prob=np.exp(-0.5*delt)
            if np.random.rand()<prob:
                accept=True
            else:
                accept=False
        if accept: 
            cur_pos=new_pos
            cur_chisq=new_chisq
        params[i,0:-1]=cur_pos
        params[i,-1]=cur_chisq
    return params
    
    
if __name__ == '__main__':
    
    t=np.arange(-5,5,0.01)
    data=Lorentzian(t,a=5)
    
    guess=np.array([1.2,0.3,0.3,-0.2])
    scale=np.array([0.1,0.1,0.1,0.1])
    nstep=100000
    chain=run_mcmc(data,guess,nstep,scale)
    nn=int(np.round(0.2*nstep)) 
    chain=chain[nn:,:] #removing the first few bad values
    

    true_param=np.array([data.a,data.b,data.c])
    for i in range(0,true_param.size):
        val=np.mean(chain[:,i])
        scat=np.std(chain[:,i])
        print(true_param[i],val,scat)

#It can be seen that the mean values returned by the chain are close to the true parameters 