#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truncated tensor Schatten p-norm based low-rank tensor completion, LRTC-TSpN

@author: nietong
"""

import numpy as np
import matplotlib.pyplot as plt
from Helper import Fold,Unfold,compute_MAE,compute_RMSE,compute_MAPE

#Optiminize Truncated Schatten p-norm via ADMM

def truncation(unfoldj,theta):
    #calculate the truncation of each unfolding
    dim = np.array(unfoldj.shape)
    wj = np.zeros(min(dim),)
    r = np.int(np.ceil(theta * min(dim)))
    wj[r:] = 1    
    
    return wj


def GST(sigma,w,p,J=5):  #J is the ineer iterations of GST, J=5 is supposed to be enough
    #Generalized soft-thresholding algorithm
    if w == 0:
        Sp = sigma
    else:
        dt = np.zeros(J+1)
        tau = (2*w*(1-p))**(1/(2-p)) + w*p*(2*w*(1-p))**((p-1)/(2-p))
        if np.abs(sigma) <= tau:
            Sp = 0
        else:
            dt[0] = np.abs(sigma)
            for k in range(J):
                dt[k+1] = np.abs(sigma) - w*p*(dt[k])**(p-1)
            Sp = np.sign(sigma)*dt[k].item()

    return Sp


def update_Mi(mat,alphai,beta,p,theta):
    #update M variable
    delta = []
    u,d,v = np.linalg.svd(mat,full_matrices=False)
    wi = truncation(mat,theta)
    for j in range(len(d)):
        deltaj = GST(d[j],(alphai/beta)*wi[j],p)
        delta.append(deltaj)
    delta = np.diag(delta)
    Mi = u@delta@v
    
    return Mi


def TSpN_ADMM(X_true,X_missing,Omega,alpha,beta,incre,maxIter,epsilon,p,theta):
    X = X_missing.copy()
    X[Omega==False] = np.mean(X_missing[Omega]) #Initialize with mean values
    errList = []
    MAE_List = []
    RMSE_List = []
    dim = X_missing.shape
    M = np.zeros(np.insert(dim, 0, len(dim))) #M is a 4-th order tensor
    Q = np.zeros(np.insert(dim, 0, len(dim))) #Q is a 4-th order tensor
    print('TSp_ADMM Iteration:     ')  
    
    for k in range(maxIter):
        beta = beta * (1+incre) #Increase beta with given step
        print(f'\r Processing loop {k}',end = '',flush=True)
        
        #Update M variable
        for i in range(np.ndim(X_missing)):
            M[i] = Fold(update_Mi(Unfold(X+(1/beta)*Q[i],dim,i),alpha[i],beta,p,theta),dim,i) ##M为四维张量
        
        Xlast = X.copy() 
        X = np.sum(beta*M-Q,axis=0)/(beta*(X_missing.ndim)) #Updata X variable
        X[Omega] = X_missing[Omega] #Observed data
        
        Q = Q + beta*(np.broadcast_to(X, np.insert(dim, 0, len(dim)))-M) #Update Q variable
        
        errList_k = np.linalg.norm(X-Xlast)/np.linalg.norm(Xlast)
        errList.append(errList_k)
        MAE_List.append(compute_MAE(X_missing,X_true,X)) 
        RMSE_List.append(compute_RMSE(X_missing,X_true,X)) 
        
        if errList_k < epsilon:
            break
           
    print(f'\n total iterations = {k}   error={errList[-1]}')
    
    return X,MAE_List,RMSE_List,errList,k


def LRTC_TSpN(complete_tensor,observed_tensor,theta=0.1,alpha=np.array([1,1,1]),p=0.5,beta=1e-5,incre=0.05,maxiter = 200,show_plot = True):
    X_true = complete_tensor.copy()
    X_missing = observed_tensor.copy()
    Omega = (X_missing != 0)
    alpha = alpha.reshape(-1,1)
    alpha = alpha / np.sum(alpha)
    epsilon = 1e-3
    X_hat,MAE_List,RMSE_List,errList,it = TSpN_ADMM(X_true,X_missing,Omega,alpha,beta,incre,maxiter,epsilon,p,theta)
    MAPE = compute_MAPE(X_missing,X_true,X_hat)
    print(f'LRTC-TSpN imptation MAE = {MAE_List[-1]:.3f}')
    print(f'LRTC-TSpN imputation RMSE = {RMSE_List[-1]:.3f}')
    print(f'LRTC-TSpN imputation MAPE = {MAPE:.3f}')
    
    if show_plot == True:
        plt.plot(range(len(MAE_List)),MAE_List)
        plt.xlabel('epoch')
        plt.ylabel('MAE')
        plt.title('Convergence curve of LRTC-TSpN')
        
    return it,X_hat,MAE_List,RMSE_List,errList

