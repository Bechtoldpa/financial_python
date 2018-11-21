# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np


def min_var_portfolio(sigma, returns):
    """ 
    Parameters
    ==========
    sigma = Variance, Covariance Matrix
    returns = vector of asset returns"""
    top_mat = 2 * sigma
    A = np.ones([len(sigma)+1, len(sigma) + 1])
    A[:-1,:-1] = top_mat
    A[-1,-1] = 0
    b = np.zeros(len(sigma))
    b = np.append(b, 1)    
    
    Z = np.dot(np.linalg.inv(A),b)
    m = Z[:-1]
    
    return m

def portfolio_returns(mu, weimghts):
    ret = np.dot(weights.T,mu)
    return ret
if __name__==__main__:
    sigma = np.matrix([[0.01, 0.0018, 0.0011],[0.0018, 0.0109, 0.0026],[0.0011, 0.0026, 0.0199]])
    mu = np.matrix([[0.0427],[0.0015],[0.0285]])