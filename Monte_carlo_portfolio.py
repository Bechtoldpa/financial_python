# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 16:39:05 2017

@author: pasca
"""

import os
os.chdir("E:\GoogleDrive\Invest\Python\Portfolio\MySQLdb")

from parse_from_adj_yahoo import obtain_list_of_db_tickers
from MySql2Portfolio import retrieve_prices_from_sql, cut_sample
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime
from termcolor import colored
import MySQLdb as mdb


#%% Get Data
if __name__ == "__main__":
    prices = pd.DataFrame
    tickers = obtain_list_of_db_tickers("ETF")
    prices, rets = retrieve_prices_from_sql(tickers)
    returns = cut_sample(rets, 250)
    returns.interpolate(inplace = True)
    returns.dropna(inplace = True, axis = 1)
    #calculate moments
    mean_daily_returns = returns.mean()
    cov_matrix = returns.cov()
    # set number of runs of random portfolio weights
    num_portfolios = 25000
    
    # set up array to hold results 
    results = np.zeros((3, num_portfolios))
    weight = np.zeros((len(returns.columns), num_portfolios))
    for i in range(num_portfolios):
        # select random weights for portfolio holdings
        weights = np.random.random(len(returns.columns))
        # rebalance weights to sum to 1
        weights /= np.sum(weights)
        
        #calculate portfolio return and volatility
        portfolio_return = np.sum(mean_daily_returns * weights) * 252
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, 
                                    weights))) * np.sqrt(252)
        
        #store results in results array
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        # store Sharpe Ratio (return / volatility) - rf excluded for simplicity
        results[2,i] = results[0,1] / results[1,i]
        weight[:,i] = weights
    #convert results array to Pandas DataFrame
    results_frame = pd.DataFrame(results.T, columns = ['ret', 'stdev', 'sharpe'])
    
    #create scatter plot coloured by Sharpe Ratio
    plt.scatter(results_frame.stdev, results_frame.ret, 
                c = results_frame.sharpe, cmap='RdYlBu')
    plt.colorbar()
#%% Functions
from matplotlib.finance import quotes_historical_yahoo_ochl as getData
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
from numpy.linalg import inv, pinv
#%% 1.  Code for input area:
begYear,endYear = 2001,2013
stocks=['IBM','WMT','AAPL','C','MSFT']
#%% 2.  Code for defining two functions:
def ret_monthly(returns):  #  function 1
    #x = returns
    date=[]
    d0=returns.index
    for i in range(0,len(returns)): 
        date.append(''.join([d0[i].strftime("%Y"),d0[i].strftime("%m")]))
    y=pd.DataFrame(returns,date,columns=returns.columns)
    return y.groupby(y.index).sum()

def objFunction(W, R, target_ret):
    stock_mean=np.mean(R,axis=0) 
    port_mean=np.dot(W,stock_mean)          # portfolio mean 
    cov=np.cov(R.T)                         # var-cov matrix
    port_var=np.dot(np.dot(W,cov),W.T)     # portfolio variance 
    penalty = 2000*abs(port_mean-target_ret)# penalty 4 deviation 
    return np.sqrt(port_var) + penalty     # objective function
#%% 3.  Code for generating a return matrix R:
R0=ret_monthly(stocks[0])                   # starting from 1st 
stock 
n_stock=len(stocks)                         # number of stocks
for i in xrange(1,n_stock):                 # merge with other stocks 
    x=ret_monthly(stocks[i]) 
    R0=pd.merge(R0,x,left_index=True,right_index=True)
    R=np.array(R0)
    
#%%4.  Code for estimating optimal portfolios for a given return:
out_mean,out_std,out_weight=[],[],[] 
stockMean=np.mean(R,axis=0)
for r in np.linspace(np.min(stockMean),np.max(stockMean),num=100):
    W = np.ones([n_stock])/n_stock    # starting from equal weights 
    b_ = [(0,1) 
    for i in range(n_stock)]          # bounds, here no short 
    c_ = ({'type':'eq', 'fun': lambda W: sum(W)-1. })#constraint
    result=sp.optimize.minimize(objFunction,W,(R,r),method='SLSQP'
                                ,constraints=c_, bounds=b_)
    if not result.success:            # handle error raise 
     BaseException(result.message)
    out_mean.append(round(r,4))       # 4 decimal places 
    std_=round(np.std(np.sum(R*result.x,axis=1)),6) 
    out_std.append(std_)
    out_weight.append(result.x)
    
#%%5.  Code for plotting the efficient frontier:
plt.title('Efficient Frontier')
plt.xlabel('Standard Deviation of the porfolio (Risk))') 
plt.ylabel('Return of the portfolio') 
plt.figtext(0.5,0.75,str(n_stock)+' stock are used: ') 
plt.figtext(0.5,0.7,' '+str(stocks))
plt.figtext(0.5,0.65,'Time period: '+str(begYear)+' ------ '+str(endYear)) 
plt.plot(out_std,out_mean,'--')
plt.show()


