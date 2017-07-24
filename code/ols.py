# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:11:31 2017

@author: Lori
"""

#函数部分

import numpy as np
import pandas as pd
import statsmodels.api as sm

def predict(X,Y,x):
    '''
    @note:对X,Y做线性回归
    @X:自变量
    @Y:应变量
    @x:生成预测的x值
    '''
    X=np.array(X)
    Y=np.array(Y)
    X=sm.add_constant(X)
    model=sm.OLS(Y,X)
    results=model.fit()
    x=np.hstack(([1],np.array(x)))
    return model.predict(results.params,x)

# 数据部分
###之前
p=pd.read_csv('../data/margin_m.csv')
p.columns=['time','position_margin','commodity_pre','equity_pre','fix_pre','margin']
p.index=p.time
p.drop('time',axis=1,inplace=True)
p.dropna(how="any")#去掉无效值
p=p[p['margin']>0]#去掉无效值


###之后
p=pd.read_csv('../data/margin_m.csv',index_col=0)
p.index=[pd.Timestamp(str(x)) for x in p.index]
d=p[p>0].dropna(how="any")





p=p[-12:]#取最近一年的
print(predict(p['commodity_pre'],p['margin'],[1]))