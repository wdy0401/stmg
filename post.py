# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/07
目的： 生成6个统计范围的数据总表
"""
import re
import pandas as pd
import matplotlib.pyplot as plt

def digi2datetime(idx):
    ret=list()
    for dt in idx:
        y=int(dt/10000)
        m=int((dt-y*10000)/100)
        d=dt-y*10000-m*100
        ret.append(pd.datetime(y,m,d))
    return ret
        
future=pd.read_csv('./index.csv',names=['future'])
future.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',x).groups()]) for x in future.index]

future_settle=pd.read_csv('./future_settle.csv',names=['future_settle'])*100000000
future_settle.index=digi2datetime(future_settle.index)

security=pd.read_csv('./security.csv',names=['security'])*100000000
security.index=digi2datetime(security.index)

nonbank=pd.read_csv('./nonbank.csv',names=['nonbank'])*100000000
nonbank.index=digi2datetime(nonbank.index)

alist=pd.concat([future,future_settle,security,nonbank],axis=1)
alist=alist.ffill()
alist.plot()
plt.savefig('sum.png', dpi=100)


