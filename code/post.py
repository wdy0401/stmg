# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/19
目的： 生成6个统计范围的数据总表
从wind提取证券结算资金数据，金融机构：各项存款余额，非存款金融机构存贷款
 绘制持仓量，成交量，客户权益金图，并保存
"""
#from WindPy import *
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
#w.start();
today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
tradeall=pd.read_csv('../data/tradeall.csv',names=['tradeall'])
tradeall.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in tradeall.index]

positionall=pd.read_csv('../data/positionall.csv',names=['positionall'])
positionall.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in positionall.index]

# 证券结算资金数据
#a=w.edb("M5207489", "2012-01-01", today,"Fill=Previous")
#settlement=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T
#settlement=settlement*100000000
#settlement.columns=['settlement']
#settlement.to_csv("../data/settlement.csv")
#settlement.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in settlement.index]
settlement=pd.read_csv('../data/settlement.csv',index_col=0) # 测试使用

# 金融机构：各项存款余额
#c=w.edb("M0009940", "2012-01-01", today,"Fill=Previous")
#deposit=pd.DataFrame(c.Data,index=c.Fields,columns=c.Times).T
#deposit=deposit*100000000
#deposit.columns=['deposit']
#deposit.to_csv("../data/deposit.csv")
#deposit.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in deposit.index]
deposit=pd.read_csv('../data/deposit.csv',index_col=0) # 测试使用

# 非存款金融机构存贷款
#d=w.edb("M0252011", "2012-01-01", today,"Fill=Previous")
#nobank=pd.DataFrame(d.Data,index=d.Fields,columns=d.Times).T
#nobank=nobank*100000000
#nobank.columns=['nobank']
#nobank.to_csv("../data/nobank.csv")
#nobank.index=[pd.datetime(*[int(y) for y in re.search('(\d+)-(\d+)-(\d+)',str(x)).groups()]) for x in nobank.index]
nobank=pd.read_csv('../data/nobank.csv',index_col=0) # 测试使用

# 客户权益金
p=pd.read_csv('../data/margin.csv',names=['margin'])*100000000
p.index=[pd.Timestamp(x) for x in p.index]

# 绘图
alist=pd.concat([tradeall,positionall,settlement,p,nobank,deposit],axis=1)
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/sum.png', dpi=100)

alist=pd.concat([tradeall,positionall,settlement,p],axis=1)
alist=alist.ffill()
alist.plot()
plt.savefig('../fig/part.png', dpi=100)

#if __name__=="__main__":
#    import post
#    print(help(post))