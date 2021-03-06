# -*- coding: utf-8 -*-
"""
Created on Tue May 16 10:52:58 2017

@author: Aadila
"""

import numpy as np

def simulate_gaussian(t,sig=0.5, cent=0,amp=1):
    dat=amp*np.exp(-0.5*(t-cent)**2/sig**2)
    dat+=np.random.randn(t.size)
    return dat
    
def get_trial_offset(sigs):
    return sigs*np.random.randn(sigs.size)
    
class Gaussian:
    def __init__(self, t, offset=0, sig=0.5, cent=0, amp=1):
        self.t=t
        self.y=simulate_gaussian(t,sig,cent,amp)+offset
        self.sig=sig
        self.cent=cent
        self.amp=amp
        self.offset=offset
        self.err=np.ones(t.size)
        
    def get_chisq(self, vec):
        sig=vec[0]
        cent=vec[1]
        amp=vec[2]
        offset=vec[3]

        pred=offset+amp*np.exp(-0.5*(self.t-cent)**2/sig**2)
        chisq=np.sum((self.y-pred)**2/self.err**2)
        return chisq
        
def run_mcmc(data,start_pos,nstep,scale=None):
    nparam=start_pos.size
    params=np.zeros([nstep,nparam+1])
    params[0,0:-1]=start_pos
    cur_chisq=data.get_chisq(start_pos)
    cur_pos=start_pos.copy()
    totaccept=0
    totreject=0
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
            totaccept=totaccept+1
            cur_pos=new_pos
            cur_chisq=new_chisq
        else:
            totreject=totreject+1
        params[i,0:-1]=cur_pos
        params[i,-1]=cur_chisq
        accept_frac=totaccept/(totaccept+totreject)
    return params,accept_frac
    
    
if __name__ == '__main__':
    
    t=np.arange(-5,5,0.1)
    data=Gaussian(t,amp=2.5)
    guess=np.array([0.3,0.3,1.2,-0.2])
    nstep=1000
    scale=np.array([0.1,0.1,0.1,0.1])
    chain,accept =run_mcmc(data,guess,nstep,scale)
    nn=int(np.round(0.0*nstep))
    chain=chain[nn:,:]
    
    scale2=np.std(chain[:,0:-1],0) #Take sd of each column, gives error in each parameter
    nstep2=100000
    chain2,accept2=run_mcmc(data,chain[-1,0:-1],nstep2,scale2)
    nn2=int(np.round(nstep2*0.2))
    chain2=chain2[nn2:,:]

    print ("Accept fraction for short chain = " + repr(accept))
    print ("Accept fraction for long chain = "+ repr(accept2))
   
    real_param=np.array([data.sig,data.cent, data.amp,data.offset])
    for i in range (0, real_param.size):
        val=np.mean(chain2[:,i])    
        scat=np.std(chain2[:,i])
        print( real_param[i],val,scat)
  
 #Accept fraction for long chain is relatively close to 0.25