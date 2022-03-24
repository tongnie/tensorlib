#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tools for tensor operations

@author: nietong
"""

import numpy as np
from collections import deque
import matplotlib.pyplot as plt


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


def tensor2mat(tensor):
    #convert a tensor into a matrix by flattening the 'day' mode to 'time interval'.
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

