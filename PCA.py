# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 20:33:04 2018

@author: Pascal
"""

#%% Principal Component analysis

import numpy as np
import pandas as pd
import pandas_datareader.data as web
from sklearn.decomposition import KernelPCA


symbols = ['ADS.DE', 'BMW.DE','DBK.DE','FRE.DE','LIN.DE',
        'SAP.DE','ALV.DE','CBK.DE','DPW.DE','HEI.DE','LXS.DE',
        'SDF.DE','BAS.DE', 'BAYN.DE', 'BEI.DE','CON.DE', 'DAI.DE', 'DB1.DE',
        'DTE.DE', 'EOAN.DE', 'FME.DE','HEN3.DE', 'IFX.DE', 'LHA.DE',
        'MRK.DE', 'MUV2.DE', 'RWE.DE','SIE.DE', 'TKA.DE', 'VOW3.DE',
        '^GDAXI']
#    
#%time 
data = pd.DataFrame()
for sym in symbols:
    data[sym] = web.DataReader(sym, data_source='yahoo')['Close']

data = data.dropna()

dax = pd.DataFrame(data.pop('^GDAXI'))

data[data.columns[:6]].head()

#%% Applying PCA



scale_function = lambda x: (x - x.mean()) / x.std()

pca = KernelPCA().fit(data.apply(scale_function))
len(pca.lambdas_)

pca.lambdas_[:10].round()

get_we = lambda x: x / x.sum()
get_we(pca.lambdas_)[:10]

get_we(pca.lambdas_)[:5].sum()

pca = KernelPCA(n_components=1).fit(data.apply(scale_function))
dax['PCA_1'] = pca.transform(-data)

import matplotlib.pyplot as plt
dax.apply(scale_function).plot(figsize=(8, 4))

#%%
pca = KernelPCA(n_components=5).fit(data.apply(scale_function))
pca_components = pca.transform(-data)
weights = get_we(pca.lambdas_)
dax['PCA_5'] = np.dot(pca_components, weights)

import matplotlib.pyplot as plt
#%matplotlib inline
dax.apply(scale_function).plot(figsize=(8, 4))
#%%
import matplotlib as mpl
mpl_data = pd.DatetimeIndex.to_pydatetime(data.index)

mpl_dates = mpl.dates.date2num(mpl_data )
mpl_dates


#%%
plt.figure(figsize=(8, 4))
plt.scatter(dax['PCA_5'], dax['^GDAXI'], c=mpl_dates)
lin_reg = np.polyval(np.polyfit(dax['PCA_5'],
                                dax['^GDAXI'], 1),
                                dax['PCA_5'])
plt.plot(dax['PCA_5'], lin_reg, 'r', lw=3)
plt.grid(True)
plt.xlabel('PCA_5')
plt.ylabel('^GDAXI')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
                 format=mpl.dates.DateFormatter('%d %b %y'))

#%% Cutting Data

cut_date = '2011/7/1'
early_pca = dax[dax.index < cut_date]['PCA_5']
early_reg = np.polyval(np.polyfit(early_pca,
                    dax['^GDAXI'][dax.index < cut_date],1),
                    early_pca)

#mid_date = '2015/5/20'
#mid_pca = dax.all(cut_date <= dax.index < mid_date)['PCA_5']
#mid_reg = np.polyval(np.polyfit(mid_pca,
#                    dax['^GDAXI'][cut_date <= dax.index < mid_date], 1),
#                    mid_pca)



late_pca = dax[dax.index >= cut_date]['PCA_5']
late_reg = np.polyval(np.polyfit(late_pca,
                    dax['^GDAXI'][dax.index >= cut_date], 1),
                    late_pca)

plt.figure(figsize=(8, 4))
plt.scatter(dax['PCA_5'], dax['^GDAXI'], c=mpl_dates)
plt.plot(early_pca, early_reg, 'r', lw=3)
plt.plot(late_pca, late_reg, 'r', lw=3)
plt.grid(True)
plt.xlabel('PCA_5')
plt.ylabel('^GDAXI')
plt.colorbar(ticks=mpl.dates.DayLocator(interval=250), 
             format=mpl.dates.DateFormatter('%d %b %y'))