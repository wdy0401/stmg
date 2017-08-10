# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/31
目的：从wind提取证券结算资金数据，金融机构：各项存款余额，非存款金融机构存贷款，三大类wind指数;绘制持仓量，成交量，客户权益金图 
"""
from WindPy import *
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
w.start();
today = time.strftime('%Y-%m-%d',time.localtime())
tradeall=pd.read_csv('../data/trade.csv',index_col=0)['ALL']
tradeall=tradeall.rename(columns={'ALL':'trade'})
tradeall.index=[pd.Timestamp(x[0:10]) for x in tradeall.index]
position=pd.read_csv('../data/position.csv',index_col=0)
position.index=[pd.Timestamp(x[0:10]) for x in position.index]
positionall=position['ALL']

data=pd.DataFrame()
for i in ["M5207489","M0009940","M0001726",'IF.CFE','TF.CFE','CCFI.WI'] :
    a=w.edb(i, "2012-01-01", today,"Fill=Previous")
    settlement=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T
    settlement=settlement.resample('M').mean()
    settlement=settlement*100000000   
    data=pd.concat([data,settlement],axis=1)
    #print(settlement)
data.columns=("settlement","deposit","nobank","equity_index","fix_index","commondity_index")
#data.columns=("证券结算金","金融机构：各项存贷款余额","其他存款性公司：对其他金融性公司负债","沪深300期货","5年期国债期货","wind商品指数")
data.index=[pd.Timestamp(x) for x in data.index]
data.to_csv("../data/boundary.csv")
#
#data=pd.read_csv('../data/boundary.csv',index_col=0) #测试使用
#data.index=[pd.Timestamp(x[0:10]) for x in data.index] #测试使用

data2=pd.DataFrame()
for i in ['IF.CFE','TF.CFE','CCFI.WI'] :
    a=w.edb(i, "2012-01-01", today,"Fill=Previous")
    settlement=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T
#    settlement=settlement.resample('M').mean()
    settlement=settlement*100000000   
    data2=pd.concat([data2,settlement],axis=1)
    #print(settlement)
data2.columns=("equity_index","fix_index","commondity_index")
#data2.columns=("沪深300期货","5年期国债期货","wind商品指数")
data2.index=[pd.Timestamp(x) for x in data2.index]
data2.to_csv("../data/wind_index.csv")
data_index=pd.read_csv('../data/wind_index.csv',index_col=0)#测试使用，读入wind商品指数日频数据

  


###客户权益金
marginreal=pd.read_csv('./marginreal.csv',names=['marginreal'])

alist=pd.concat([tradeall,positionall,marginreal,data],axis=1)
#alist.index=[pd.Timestamp(x) for x in alist.index]
alist.columns=["tradeall","positionall","marginreal","settlement","deposit","nobank","equity_index","fix_index","commondity_index"]
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/sum.png', dpi=100)

alist=pd.concat([tradeall,positionall,marginreal],axis=1)
alist.columns=("tradeall","positionall","marginreal")
alist.index=[pd.Timestamp(x) for x in alist.index]
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/part.png', dpi=100)