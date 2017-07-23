# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:26:49 2017

@author: admin
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import statsmodels.api as sm
'''
def fix_wind_index(wdata):
    wdata.index=[pd.Timestamp(x) for x in wdata.index]
    return wdata

a=pd.read_csv("./test1.csv",index_col=0)
a=fix_wind_index(a)

#
a.to_csv('./test2.csv')
b=pd.read_csv('./test2.csv',index_col=0)
p=a['CLOSE'].resample("M").mean()
#p=b['CLOSE'].resample("M").mean()

a.to_hdf('tmp.h5','table')
c=pd.read_hdf('tmp.h5','table')
p=c['CLOSE'].resample("M").mean()
'''



#p=b['CLOSE'].resample("M").mean()
#p=b['CLOSE'].resample("M").mean()
#
#p=pd.Timestamp(20100101)
#n=30
#x=np.random.rand(n,3)
#x1=np.random.rand(n)
#Y=10+50*x[:,2]+0.01*np.random.rand(n)
#X=sm.add_constant(x)
model = sm.OLS(Y,X)
results = model.fit()
print(results.params)
print(results.summary())
f=lambda x: model.predict(results.params,x)


n=30
X=np.random.rand(n,3)
Y=10+50*X[:,2]+0.01*(np.random.rand(n)-0.5)

def predict(X,Y,x):
    X=np.array(X)
    Y=np.array(Y)
    x=np.hstack(([1],np.array(x)))
    print(x)
    X=sm.add_constant(X)
    model=sm.OLS(Y,X)
    results=model.fit()
    return model.predict(results.params,x)
for i in range(10):  
    print(predict(X,Y,[1,1,i]))


p=pd.read_csv('../data/premium.csv',names=['premium'])*100000000
p.index=[pd.Timestamp(str(x)) for x in p.index]
p=p.resample('M').mean()

c=pd.read_csv('../data/equity_pre.csv',names=['equity_pre'])
c.index=[pd.Timestamp(x) for x in c.index]
c=c.resample('M').mean()

d=pd.concat([p,c],axis=1)
d.dropna(how="any")
d=d[d['premium']>0]

print(predict(d['premium'],d['equity_pre'],[1]))


#y_fitted = results.fittedvalues
#fig, ax = plt.subplots(figsize=(8,6))
#ax.plot(x, Y, 'o', label='data')
#ax.plot(x, y_fitted, 'r--.',label='OLS')
#ax.legend(loc='best')
#


#
#from sklearn.linear_model import LinearRegression
#
#model=LinearRegression()
#x=[[i] for i in X[:,2]]
#Y=[[i] for i in Y]
#model.fit(x,Y)
#print(model.predict(12))
#print(model.predict(1))
