# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 09:09:03 2017

@author: Lori
"""
#从wind提取证券结算资金数据，金融机构：各项存款余额，非存款金融机构存贷款
# 绘制持仓量，成交量，客户权益金图
from WindPy import *
import pandas as pd
import re
import time
import numpy
import matplotlib.pyplot as plt
w.start();
today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
tradeall=pd.read_csv('../data/tradeall.csv',names=['tradeall'])
tradeall.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in tradeall.index]

positionall=pd.read_csv('../data/positionall.csv',names=['positionall'])
positionall.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in positionall.index]

#证券结算资金数据
a=w.edb("M5207489", "2012-01-01", today,"Fill=Previous")
settlement=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T
settlement=settlement*100000000
settlement.to_csv("../data/settlement.csv")
settlement.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in settlement.index]

#金融机构：各项存款余额
c=w.edb("M0009940", "2012-01-01", today,"Fill=Previous")
deposit=pd.DataFrame(c.Data,index=c.Fields,columns=c.Times).T
deposit=deposit*100000000
deposit.to_csv("../data/deposit.csv")
deposit.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in deposit.index]

#非存款金融机构存贷款
d=w.edb("M0252011", "2012-01-01", today,"Fill=Previous")
nobank=pd.DataFrame(d.Data,index=d.Fields,columns=d.Times).T
nobank=nobank*100000000
nobank.to_csv("../data/nobank.csv")
nobank.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in nobank.index]

#客户权益金
premium=pd.read_csv('../data/premium.csv',names=['premium'])*100000000
premium.index=[pd.Timestamp(str(x)) for x in premium.index]
premium.to_csv("../data/premium_w.csv")

alist=pd.concat([tradeall,positionall,settlement,premium,nobank,deposit],axis=1)
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/sum.png', dpi=100)

alist=pd.concat([tradeall,positionall,settlement,premium],axis=1)
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/part.png', dpi=100)