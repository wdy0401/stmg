# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/08/10
目的： 考虑日频的周度数据的季节性
"""

import pandas as pd
import numpy as np
from datetime import datetime

def loadcsv(filename):
    re=pd.read_csv(filename,index_col=0)
    re.index=[pd.Timestamp(x[0:10]) for x in re.index]
    re.index=[datetime(x.year,x.month,x.day) for x in re.index] 
    return re
def toidx(p):
    re=p.weekofyear+p.year*100
    if p.month==12 and p.week==1:
        re=re+100
    return re 
a=loadcsv("../data/position.csv")
ind=a.index
indweek=[x.weekday() for x in ind]
a['ind']=indweek
mean=a.groupby('ind').mean()
std=a.groupby('ind').std()

a['weekseq']=[toidx(x) for x in ind]
mean=a.groupby('weekseq').mean()

m2=a.groupby('weekseq').transform('mean')
a['dif']=a['ALL']-m2['ALL']
a.groupby('ind').mean()

diff=a[['dif','ind']]
diff.groupby('ind').mean()
diff.groupby('ind').std()

#频度图
w1=diff[diff['ind']==4]#周五的
sortnum=1000000000
w1['int']=[int(x/sortnum) for x in w1['dif']]

x=w1.groupby('int').count()
x['ind'].plot(kind='bar',figsize=(24,12))