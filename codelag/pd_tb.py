# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/24
目的：数据转化为txt固定格式
"""
import pandas as pd
from datetime import datetime
__all__=['pd_tb']

def loadcsv(filename):
    re=pd.read_csv(filename,index_col=0)
    re.index=[pd.Timestamp(x[0:10]) for x in re.index]
    re.index=[datetime(x.year,x.month,x.day) for x in re.index] 
    return re

# 函数部分
def pd_tb(p,t):
    '''
    @note:将数据转化为txt固定格式
    --------------------------
    Example：
    [20170501]
    Position_margin=44433618363.0
    Commodity_pre=34204146093.6
    Equity_pre=8694185209.36
    Fix_pre=1535287060.0
    Margin=430101000000.0
    Volume=7777
    Oi=7777
    --------------------------
    '''
    pl=""
    plist=list()
    for date in p.index:
        plist.append(f"[{date.strftime('%Y%m%d')}]")
        for name in p.columns:
            plist.append(str(name)+"="+str(p.loc[date,name]))
        if "volume" not in [str.lower(str(x)) for x in p.columns]:
            plist.append("volume=7777")
        if "oi" not in [str.lower(str(x)) for x in p.columns]:
            plist.append("oi=7777")
    for line in plist:
#        c=print(line.capitalize())
        c=line.capitalize()
        pl=pl+c+'\n'
    with open(f'../data/{t}.txt',"w") as f:
        f.write(pl)
#第一个txt
p=loadcsv('../data/wind_index.csv')
q=loadcsv('../data/position.csv')
data1=pd.concat([p['commondity_index'],q['commodity']],axis=1)
data1=data1[data1>0].dropna(how="any")
pd_tb(data1,'com_position_index')
#第二个txt
c=loadcsv('../daily/com_6_2_0.csv')
data2=pd.concat([c['0'],q['commodity']],axis=1)
data2=data1[data1>0].dropna(how="any")
pd_tb(data2,'predict_com')


#if __name__=="__main__":
#    import pd_tb
#    print(help(pd_tb))