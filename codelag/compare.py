# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/30
目的： 生成持仓保证金与客户权益金对比数据
a为持仓保证金总数，大宗商品持仓保证金总数，权益持仓保证金总数，固收保证金总说数，p为客户权益金数据
#时间选用月度数据，日期全部整合为1
"""
import pandas as pd
from datetime import datetime
#__all__=[]
b=pd.DataFrame()
a=pd.read_csv('../data/margin.csv',index_col=0)
a.index=[pd.Timestamp(x) for x in a.index]
for y in a.columns:
    b[y]=a[y].resample('M').mean()
b.index=[datetime(x.year,x.month,1) for x in b.index]
p=pd.read_csv('./marginreal.csv',names=['marginreal'])
p.index=[pd.Timestamp(x) for x in p.index]
p.index=[datetime(x.year,x.month,1) for x in p.index]
e=pd.concat([b,p],axis=1)['2013':p.index[-1]]
e.to_csv('../data/margin_compare.csv')

#if __name__=="__main__":
#    import compare
#    print(help(compare))