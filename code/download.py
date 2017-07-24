# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/24
目的：生成每日的期货交易量数据
注释：
    wind成交额的计算方式
    zj 单边
    sq 双边
    ds 双边
    zs 双边
"""

import os
import re
import pandas as pd
from datetime import datetime
#from WindPy import *

global persym;persym=dict()
global ctrs_data;ctrs_data=dict() #存储本次下载的所有信息
global sym_index;sym_index=dict()
global mtpr;mtpr=dict()
global ratio;ratio=dict()
__all__=['getctrs','download','get_mtpr','load_mtpr','fix_mtpr','roll','merge','download_all',
         'merge_all','to_disk','merge2','merge_all2','to_disk2','get_ratio','merge3','merge_all3']

# 初始化
def init():
    '''
    @note:初始化函数,生成对应文件夹
    '''
#    w.start()
    if not os.path.exists('../raw'):
        os.mkdir('../raw')
    if not os.path.exists('../fig'):
        os.mkdir('../fig')
    if not os.path.exists('../data'):
        os.mkdir('../data')

def getctrs():
    '''
    @note:生成所有的wind合约名
    '''
    with open("ctrlist.txt") as f:
        for line in f.readlines():
            yield line.strip()

def download(ctr,sym): 
    '''
    @note:下载所有的合约相关数据,包括收盘，成交，总量，持仓，结算
    @ctr:合约名
    @sym:品种名
    '''
#   today=datetime.today()
#   a=w.wsd(ctr, "close,volume,amt,oi,settle", "2008-01-01", f"{today.year}-{today.month}-{today.day}", "")#收盘 成交 总量 持仓 结算
#   df=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T # 转换成pd格式
#   df.to_csv(f"../raw/{ctr}.csv") #存储到本地
    df=pd.DataFrame.from_csv(f"../raw/{ctr}.csv") #测试时使用
    if sym not in ctrs_data:
        ctrs_data[sym]=dict()    
    ctrs_data[sym][ctr]=df.copy() #存储到ctrs_data
    sym_index[sym]=df.index

def get_mtpr(sym): 
    '''
    @note:返回合约乘数
    '''
    global mtpr
    return mtpr[sym]

def load_mtpr():
    '''
    @note:提取品种合约乘数与保证金
    '''
    global mtpr
    global ratio
    with open("./symbol_info.csv") as f:
        for line in f.readlines():
            lst=line.strip().split(',')
            mtpr[lst[0].upper()]=float(lst[4])
            ratio[lst[0].upper()]=float(lst[2])

def fix_mtpr(sym):
    '''
    @note:对合约乘数变化过的品种乘数进行处理，方法为：在变化时间段内按照线性变化做平滑处理
    '''
    global sym_index
    global mtpr
    idx=sym_index[sym]
    tmp_mtpr=pd.DataFrame([1 for x in range(0,len(idx))],index=idx)
    if sym=='PB':
        roll(tmp_mtpr,idx[0],"2012-09-20",25,25)
        roll(tmp_mtpr,"2012-09-20","2013-08-16",25,5)
        roll(tmp_mtpr,"2013-08-16",idx[-1],5,5)
    if sym=='RU':
        roll(tmp_mtpr,idx[0],"2011-08-16",5,5)
        roll(tmp_mtpr,"2011-08-16","2012-07-18",5,10)
        roll(tmp_mtpr,"2012-07-18",idx[-1],10,10)
    if sym=='FU':
        roll(tmp_mtpr,idx[0],"2011-01-03",10,10)
        roll(tmp_mtpr,"2011-01-03","2011-11-31",10,50)
        roll(tmp_mtpr,"2011-11-31",idx[-1],50,50)
    if sym=='WH':
        roll(tmp_mtpr,idx[0],"2012-06-01",50,50)
        roll(tmp_mtpr,"2012-06-01","2013-04-30",50,20)
        roll(tmp_mtpr,"2013-04-30",idx[-1],20,20)
    if sym=='MA':
        roll(tmp_mtpr,idx[0],"2014-06-01",50,50)
        roll(tmp_mtpr,"2014-06-01","2015-04-30",50,10)
        roll(tmp_mtpr,"2015-04-30",idx[-1],10,10)
    if sym=='ZC':
        roll(tmp_mtpr,idx[0],"2015-05-06",200,200)
        roll(tmp_mtpr,"2015-05-06","2016-03-30",200,100)
        roll(tmp_mtpr,"2016-03-30",idx[-1],100,100)
    if sym=='RI':
        roll(tmp_mtpr,idx[0],"2012-06-01",10,10)
        roll(tmp_mtpr,"2012-06-01","2013-04-30",10,20)
        roll(tmp_mtpr,"2013-04-30",idx[-1],20,20) 
    if sym=='RS':
        roll(tmp_mtpr,idx[0],"2012-06-01",5,5)
        roll(tmp_mtpr,"2012-06-01","2013-04-30",5,10)
        roll(tmp_mtpr,"2013-04-30",idx[-1],10,10) 
    if sym==['IF','IH']:
        roll(tmp_mtpr,idx[0],"2015-08-01",10,10)
        roll(tmp_mtpr,"2015-08-01","2015-09-01",10,20)
        roll(tmp_mtpr,"2015-09-01","2015-09-07",20,20)
        roll(tmp_mtpr,"2015-09-07","2015-09-07",20,30)
        roll(tmp_mtpr,"2015-09-07","2017-02-17",30,30)
        roll(tmp_mtpr,"2017-02-17","2017-02-17",30,20)
        roll(tmp_mtpr,"2017-02-17",idx[-1],20,20) 
    if sym=='IC':
        roll(tmp_mtpr,idx[0],"2015-08-01",10,10)
        roll(tmp_mtpr,"2015-08-01","2015-09-01",10,20)
        roll(tmp_mtpr,"2015-09-01","2015-09-07",20,20)
        roll(tmp_mtpr,"2015-09-07","2015-09-07",20,30)
        roll(tmp_mtpr,"2015-09-07","2017-02-17",30,30)
        roll(tmp_mtpr,"2017-02-17","2017-02-17",30,25)
        roll(tmp_mtpr,"2017-02-17",idx[-1],25,25) 
    mtpr[sym]=tmp_mtpr.copy()

def roll(rollmtpr,bt,et,bm,em):
    '''
    @note:对改变过合约的乘数进行线性平滑运算
    @rollmtpr：合约乘数
    @bt:乘数开始变化时间
    @et:乘数结束变化时间
    @bm:初始合约乘数
    @em:变动后合约乘数
    '''
    tmp_index=rollmtpr[bt:et].index
    length=len(tmp_index)
    for i,tidx in enumerate(tmp_index):
        rollmtpr[tidx:tidx]=((length-i)*bm+i*em)/length    

def merge(sym,ctrs): 
    '''
    @note:合并单品种的成交量
    只有中金所是单边计算 其余均为双边计算
    '''
    global persym
    df=pd.concat([ctr['VOLUME']*ctr['SETTLE']*get_mtpr(sym) for ctr in ctrs.values()],axis=1)
    if sym not in ['IF','IH','IC','TF','T']: #只有中金所是单边计算 其余均为双边计算
        df=df/2
    persym[sym]=df.sum(1) #按日合并数据

def download_all(): 
    '''
    @note:下载所有品种的量价数据 
    '''
    for ctr in getctrs():
        sym=re.search('(\D+)',ctr).group(0)
        download(ctr,sym)

def merge_all():
    '''
    @note:分品种合成成交量数据
    '''
    for sym in ctrs_data.keys():
        merge(sym,ctrs_data[sym])
    equity=0
    for sym in ['IF','IH','IC']:
        equity=equity+persym[sym]
    equity.to_csv("../data/equity_trade.csv") 
    fix=0
    for sym in ['TF','T']:
        fix=fix+persym[sym]
    fix.to_csv("../data/fix_trade.csv")
    comm=0
    for sym in persym.keys():
        comm=comm+persym[sym]
    comm=comm-equity-fix
    comm.to_csv("../data/commodity_trade.csv")

def to_disk():
    '''
    @note:储存各品种成交量数据，以及每日成交总额
    '''
    global persym
    df=pd.concat([pd.DataFrame(x) for x in persym.values()],axis=1)
    df.columns=persym.keys()
    df.to_csv("../data/trade.csv")    
    df.sum(1).to_csv("../data/tradeall.csv") #按行合并计算每日成交额
    
def merge2(sym,ctrs):
    '''
    @note:合并单品种的持仓额
    '''
    global persym
    df=pd.concat([ctr['SETTLE']*ctr['OI']*get_mtpr(sym) for ctr in ctrs.values()],axis=1)
    if sym not in ['IF','IH','IC','TF','T']: #只有中金所是单边计算 其余均为双边计算
        df=df/2
    persym[sym]=df.sum(1) #按日合并数据

def merge_all2(): 
    '''
    @note:综合所有的持仓额数据,分品种计算持仓金额
    '''
    for sym in ctrs_data.keys():
        merge2(sym,ctrs_data[sym])
    equity=0
    for sym in ['IF','IH','IC']:
        equity=equity+persym[sym]
    equity.to_csv("../data/equity_position.csv") 
    fix=0
    for sym in ['TF','T']:
        fix=fix+persym[sym]
    fix.to_csv("../data/fix_position.csv")
    comm=0
    for sym in persym.keys():
        comm=comm+persym[sym]
    comm=comm-equity-fix
    comm.to_csv("../data/commodity_position.csv")

def to_disk2():
    '''
    @note:储存各品种每日持仓额数据以及每日总持仓额数据
    '''
    global persym
    df=pd.concat([pd.DataFrame(x) for x in persym.values()],axis=1)
    df.columns=persym.keys()
    df.to_csv("../data/position.csv")
    df.sum(1).to_csv("../data/positionall.csv")#按行合并计算每日持仓额
    
def get_ratio(sym):
    '''
    @note:提取品种保证金数据
    '''
    global ratio
    return ratio[str.upper(sym)]

def merge3(sym,ctrs):
    '''
    @note:按保证金计算持仓数据,合并单品种的持仓保证金以及每日持仓保证金
    '''
    global persym
    df=pd.concat([ctr['OI']*ctr['SETTLE']*get_mtpr(sym)*get_ratio(sym) for ctr in ctrs.values()],axis=1)
    if sym not in ['IF','IH','IC','TF','T']:#只有中金所是单边计算 其余均为双边计算
        df=df/2
    persym[sym]=df.sum(1) #按日合并数据
    
def merge_all3():
    '''
    @note:分品种计算持仓保证金,综合所有的持仓额数据
    '''
    global persym
    for sym in ctrs_data.keys():
        merge3(sym,ctrs_data[sym])         
    equity=0
    for sym in ['IF','IH','IC']:
        equity=equity+persym[sym]
    equity.to_csv("../data/equity_pre.csv") 
    fix=0
    for sym in ['TF','T']:
        fix=fix+persym[sym]
    fix.to_csv("../data/fix_pre.csv")
    comm=0
    for sym in persym.keys():
        comm=comm+persym[sym] 
    comm.to_csv("../data/position_margin.csv")
    comm=comm-equity-fix
    comm.to_csv("../data/commodity_pre.csv")

init() 
download_all()
load_mtpr()
merge_all()
to_disk()
merge_all2()
to_disk2()
merge_all3()

if __name__=="__main__":
    import download
    print(help(download))
    