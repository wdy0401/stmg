# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/24
目的：OLS线性回归，预测客户权益金数据
"""
'''
对于每个日期 需要得到的数据为
    当日保证金的绝对额
    用于预测的历史数据
'''

import numpy as np
import pandas as pd
import re
import statsmodels.api as sm

__all__=['predict']

# 函数部分
def predict(X,Y,x):
    '''
    @note:对X,Y做线性回归，并得到预测值
    @X:自变量
    @Y:应变量
    @x:输入x值求预测值
    '''
    X=np.array(X)
    Y=np.array(Y)
    X=sm.add_constant(X)
    model=sm.OLS(Y,X)
    results=model.fit()
    x=np.hstack(([1],np.array(x)))
#    return results.summary()
    return model.predict(results.params,x)

# 数据部分
p=pd.read_csv('../data/margin_m.csv', index_col=0)
p.index=[pd.Timestamp(str(x)) for x in p.index]
d=p[p>0].dropna(how="any")#去掉无效值
d=d[-12:]#取最近一年的
print(predict(d['commodity_pre'],d['margin'],[1]))

if __name__=="__main__":
    import ols
    print(help(ols))