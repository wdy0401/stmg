# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 09:09:03 2017

@author: Lori
"""

from WindPy import *
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
w.start();
today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
def digi2datetime(idx):
    ret=list()
    for dt in idx:
        y=int(dt/10000)
        m=int((dt-y*10000)/100)
        d=dt-y*10000-m*100
        ret.append(pd.datetime(y,m,d))
    return ret
tradeall=pd.read_csv('../data/tradeall.csv',names=['tradeall'])
tradeall.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in tradeall.index]

positionall=pd.read_csv('../data/positionall.csv',names=['positionall'])
positionall.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in positionall.index]

#证券结算资金数据
a=w.edb("M5207489", "2012-01-01", today,"Fill=Previous")
settlement=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T
settlement=settlement*100000000
#settlement.columns =[]
#settlement.to_csv("../data/test1.csv")
settlement.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in settlement.index]

#金融机构：各项存款余额
c=w.edb("M0009940", "2012-01-01", today,"Fill=Previous")
deposit=pd.DataFrame(c.Data,index=c.Fields,columns=c.Times).T
deposit=deposit*100000000
#deposit.to_csv("../data/test2.csv")
deposit.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in deposit.index]

#非存款金融机构存贷款
d=w.edb("M0252011", "2012-01-01", today,"Fill=Previous")
nobank=pd.DataFrame(d.Data,index=d.Fields,columns=d.Times).T
nobank=nobank*100000000
#nobank.to_csv("../data/test3.csv")
nobank.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in nobank.index]

#客户权益金
premium=pd.read_csv('../data/premium.csv',names=['premium'])*100000000
premium.index=digi2datetime(premium.index)

alist=pd.concat([tradeall,positionall,settlement,premium,nobank,deposit],axis=1)
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/sum.png', dpi=100)

alist=pd.concat([tradeall,positionall,settlement,premium],axis=1)
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/part.png', dpi=100)