# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/07
目的：生成每日的期货交易量数据
"""

import os
import re
import pandas as pd
from datetime import datetime
from WindPy import *

global persym;persym=dict()
global ctrs_data;ctrs_data=dict()#存储本次下载的所有信息
global sym_index;sym_index=dict()
global mtpr;mtpr=dict()
def init():
    w.start()
    if not os.path.exists('./raw'):
        os.mkdir('./raw')
def getctrs():#生成所有的wind合约名
    with open("ctrlist.txt") as f:
        for line in f.readlines():
            yield line.strip()
def download(ctr,sym):#下载所有的合约相关数据
#    today=datetime.today()
#    a=w.wsd(ctr, "close,volume,amt,oi,settle", "2008-01-01", f"{today.year}-{today.month}-{today.day}", "")
#    df=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T#转换成pd格式
#    df.to_csv(f"./raw/{ctr}.csv")#存储到本地
    df=pd.DataFrame.from_csv(f"./raw/{ctr}.csv")#测试时使用
    if sym not in ctrs_data:
        ctrs_data[sym]=dict()    
    ctrs_data[sym][ctr]=df.copy()#存储到ctrs_data
    sym_index[sym]=df.index
def get_mtpr(sym):#返回合约乘数
    global mtpr
    return mtpr[sym]
def load_mtpr():
    global mtpr
    with open("./symbol_info.csv") as f:
        for line in f.readlines():
            lst=line.strip().split(',')
            mtpr[lst[0].upper()]=float(lst[4])
    fix_mtpr('PB')
def fix_mtpr(sym):
    global sym_index
    global mtpr
    idx=sym_index[sym]
    tmp_mtpr=pd.DataFrame([1 for x in range(0,len(idx))],index=idx)
    if sym=='PB':
        roll(tmp_mtpr,idx[0],"2012-09-02",5,5)
        roll(tmp_mtpr,"2012-09-02","2013-09-02",5,10)
        roll(tmp_mtpr,"2013-09-02",idx[-1],10,10)
    if sym=='RU':
        roll(tmp_mtpr,idx[0],"2012-09-02",5,5)
        roll(tmp_mtpr,"2012-09-02","2013-09-02",5,10)
        roll(tmp_mtpr,"2013-09-02",idx[-1],10,10)
    if sym=='FU':
        roll(tmp_mtpr,idx[0],"2012-09-02",5,5)
        roll(tmp_mtpr,"2012-09-02","2013-09-02",5,10)
        roll(tmp_mtpr,"2013-09-02",idx[-1],10,10)
    if sym=='WH':
        roll(tmp_mtpr,idx[0],"2012-09-02",5,5)
        roll(tmp_mtpr,"2012-09-02","2013-09-02",5,10)
        roll(tmp_mtpr,"2013-09-02",idx[-1],10,10)
    if sym=='MA':
        roll(tmp_mtpr,idx[0],"2012-09-02",5,5)
        roll(tmp_mtpr,"2012-09-02","2013-09-02",5,10)
        roll(tmp_mtpr,"2013-09-02",idx[-1],10,10)
    if sym=='ZC':
        roll(tmp_mtpr,idx[0],"2015-05-03",5,5)
        roll(tmp_mtpr,"2015-05-03","2016-05-03",5,10)
        roll(tmp_mtpr,"2016-05-03",idx[-1],10,10)
    if sym=='RI':
        roll(tmp_mtpr,idx[0],"2012-09-02",5,5)
        roll(tmp_mtpr,"2012-09-02","2013-09-02",5,10)
        roll(tmp_mtpr,"2013-09-02",idx[-1],10,10)   
    mtpr[sym]=tmp_mtpr.copy()
def roll(rollmtpr,bt,et,bm,em):
        tmp_index=rollmtpr[bt:et].index
        length=len(tmp_index)
        for i,tidx in enumerate(tmp_index):
            rollmtpr[tidx:tidx]=((length-i)*bm+i*em)/length    
def merge(sym,ctrs):#合并单品种的成交量
    global persym
    df=pd.concat([ctr['VOLUME']*ctr['SETTLE']*get_mtpr(sym) for ctr in ctrs.values()],axis=1)
    if sym not in ['IF','IH','IC','TF','T']:#只有中金所是单边计算 其余均为双边计算
        df=df/2
    persym[sym]=df.sum(1)#按日合并数据
def download_all():#下载所有品种的量价数据 
    for ctr in getctrs():
        sym=re.search('(\D+)',ctr).group(0)
        download(ctr,sym)
def merge_all():#综合所有的成交量数据
    for sym in ctrs_data.keys():
        merge(sym,ctrs_data[sym])
def to_disk():
    global persym
    df=pd.concat([pd.DataFrame(x) for x in persym.values()],axis=1)
    df.columns=persym.keys()
    df.to_csv("./syms.csv")
    df.sum(1).to_csv("./index.csv")#按行合并计算每日成交额
init()
download_all()
load_mtpr()
merge_all()
to_disk()



"""
wind成交额的计算方式
zj 单边
sq 双边
ds 双边
zs 双边
"""
