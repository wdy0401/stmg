# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：量化团队
创建时间：2017/08/07
修改时间：2017/08/07
目的： 时间戳滞后一天
"""
import pandas as pd
from datetime import datetime
global day

def timetype(data):
    '''
    @note:时间戳格式处理
    '''
    data.index=[pd.Timestamp(x) for x in data.index] 
    data.index=[datetime(x.year,x.month,x.day) for x in data.index] 
    return data

def lag(data):
    '''
    @note:将日期滞后一期
    '''
    global day
    data=timetype(data)
    for x in list(range(len(day))):
        if data.index[-1]==day.index[x]:
            a=day[x+1:x+2].copy()
    data=pd.concat([data,a],axis=0)
    data=data.shift(1)
    return data[1:]

init=pd.read_csv('../data/margin.csv',index_col=0) #输入需要滞后的日频数据
day=pd.read_csv('../codelag/tradingday.csv',index_col=0) #2008-2020年交易日时间序列
day=timetype(day)

lag(init).to_csv('../data/try.csv')