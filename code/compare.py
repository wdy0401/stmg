34# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/19
目的： 生成持仓保证金与客户权益金对比数据
a为持仓保证金总数，b为大宗商品持仓保证金总数，c为权益持仓保证金总数，d为固收保证金总说数，p为客户权益金数据
#时间选用月度数据，日期全部整合为1
"""
import pandas as pd
from datetime import datetime
import re
#__all__=[]
a=pd.read_csv('../data/position_margin.csv',names=['position_margin'])
a.index=[pd.Timestamp(x) for x in a.index]
a=a.resample('M').mean()
a.index=[datetime(x.year,x.month,1) for x in a.index]
p=pd.read_csv('../data/margin.csv',names=['margin'])
p.index=[pd.Timestamp(x) for x in p.index]
p.index=[datetime(x.year,x.month,1) for x in p.index]
b=pd.read_csv('../data/commodity_pre.csv',names=['commodity_pre'])
b.index=[pd.Timestamp(x) for x in b.index]
b=b.resample('M').mean()
b.index=[datetime(x.year,x.month,1) for x in b.index]
c=pd.read_csv('../data/equity_pre.csv',names=['equity_pre'])
c.index=[pd.Timestamp(x) for x in c.index]
c=c.resample('M').mean()
c.index=[datetime(x.year,x.month,1) for x in c.index]
d=pd.read_csv('../data/fix_pre.csv',names=['fix_pre'])
d.index=[pd.Timestamp(x) for x in d.index]
d=d.resample('M').mean()
d.index=[datetime(x.year,x.month,1) for x in d.index]
e=pd.concat([a,b,c,d,p*100000000],axis=1)['2013':p.index[-1]]
e.to_csv('../data/margin_m.csv')

#if __name__=="__main__":
#    import compare
#    print(help(compare))