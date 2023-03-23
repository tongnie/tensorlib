#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools for tensor operations

@author: nietong
"""

import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import random as random


def shiftdim(array, n=None):
    if n is not None:
        if n >= 0:
            axes = tuple(range(len(array.shape)))
            new_axes = deque(axes)
            new_axes.rotate(n)
            return np.moveaxis(array, axes, tuple(new_axes))
        return np.expand_dims(array, axis=tuple(range(-n)))
    else:
        idx = 0
        for dim in array.shape:
            if dim == 1:
                idx += 1
            else:
                break
        axes = tuple(range(idx))
        # Note that this returns a tuple of 2 results


def Fold(X, dim, i):
    #Fold a matrix into a tensor in mode i, dim is a tuple of the targeted tensor.
    dim = np.roll(dim, -i)
    X = shiftdim(np.reshape(X, dim,order='F'), len(dim)-i)
    return X


def Unfold( X, dim, i ):
    #Unfold a tensor into a tensor in mode i.
    X_unfold = np.reshape(shiftdim(X,i), (dim[i],-1),order='F')
    return X_unfold


def TensorFromMat(mat,dim):
    #Construct a 3D tensor from a matrix
    days_slice = [(start_i,start_i + dim[0]) for start_i in list(range(0,dim[0]*dim[2],dim[0]))]
    array_list = []
    for day_slice in days_slice:
        start_i,end_i = day_slice[0],day_slice[1]
        array_slice = mat[start_i:end_i,:]
        array_list.append(array_slice)
        tensor3d = np.array(np.stack(array_list,axis = 0).astype('float64'))
        tensor3d = np.moveaxis(tensor3d,0,-1)

    print(tensor3d.shape)
        
    return tensor3d

    
def Tensor2Mat(tensor):
    #convert a tensor into a matrix by flattening the 'day' mode to 'time interval'.
    #The shape of given tensor should be 'time interval * locations * days'.
    #Note that this operation is slightly different from Unfold operation
    for k in range(np.shape(tensor)[-1]):
        if k == 0:
            stacked = np.vstack(tensor[:,:,k])
        else:
            stacked = np.vstack((stacked,tensor[:,:,k]))
    return stacked


def compute_MAE(X_masked,X_true,X_hat): #Only calculate the errors on the masked and nonzero positions
    pos_test = np.where((X_true != 0) & (X_masked == 0))
    MAE = np.sum(abs(X_true[pos_test]-X_hat[pos_test]))/X_true[pos_test].shape[0]
    
    return MAE


def compute_RMSE(X_masked,X_true,X_hat):
    pos_test = np.where((X_true != 0) & (X_masked == 0))
    RMSE = np.sqrt(((X_true[pos_test]-X_hat[pos_test])**2).sum()/X_true[pos_test].shape[0])
    
    return RMSE


def compute_MAPE(X_masked,X_true,X_hat): 
    pos_test = np.where((X_true != 0) & (X_masked == 0))
    MAPE = np.sum(np.abs(X_true[pos_test]-X_hat[pos_test]) / X_true[pos_test]) / X_true[pos_test].shape[0]
    
    return MAPE


def get_missing_rate(X_lost):
    o_channel_num = (X_lost == 0).astype(int).sum().sum()
    matrix_miss_rate = o_channel_num/(X_lost.size)
    
    return matrix_miss_rate


def generate_fiber_missing(tensor3d_true,lost_rate,mode:int): 
    #three kinds of fiber-like missing cases, the original tensor structure is intervals*links*days.
    #mode0:links*days combination
    #mode1:intervals*days combination
    #mode2:intervals*links combination
    n = tensor3d_true.shape
    nn = np.delete(n,mode)
    S = np.ones(nn)
    coord = []
    for i in range(nn[0]):
        for j in range(nn[1]):
            coord.append((i,j))
    mask = random.sample(coord,int(lost_rate*len(coord)))
    for coord in mask:
        S[coord[0],coord[1]] = 0
    fai = np.expand_dims(S,mode).repeat(n[mode],axis=mode)
    tensor3d_lost_fiber = fai*tensor3d_true
    tensor_miss_rate = get_missing_rate(tensor3d_lost_fiber)
    print(f'fiber-mode{mode} missing rate of tensor is：{100*tensor_miss_rate:.2f}%')

    return tensor3d_lost_fiber

def generate_tensor_random_missing(tensor3d_true,lost_rate):
    tensor3d_lost = tensor3d_true.copy()
    coord = []
    m,n,q = tensor3d_lost.shape
    for i in range(m):
        for j in range(n):
            for k in range(q):
                coord.append((i,j,k))
    
    mask = random.sample(coord,int(lost_rate*len(coord)))
    for coord in mask:
        tensor3d_lost[coord[0]][coord[1]][coord[2]] = 0
    return tensor3d_lost

