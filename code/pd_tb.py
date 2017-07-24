# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/24
目的：数据转化为txt固定格式
"""
import pandas as pd

__all__=['pd_tb']

# 函数部分
def pd_tb(p):
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
        print(line.capitalize())

p=pd.read_csv('../data/margin_m.csv',index_col=0)
p.index=[pd.Timestamp(str(x)) for x in p.index]
d=p[p>0].dropna(how="any")

pd_tb(d)

if __name__=="__main__":
    import pd_tb
    print(help(pd_tb))