# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/30
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
from WindPy import *

global persym;persym=dict()
global ctrs_data;ctrs_data=dict() #存储本次下载的所有信息
global sym_index;sym_index=dict()
global mtpr;mtpr=dict()
global ratio;ratio=dict()
__all__=['getctrs','download','get_mtpr','load_mtpr','fix_mtpr','roll','merge','download_all',
         'get_ratio']
import functools
from datetime import datetime
def betimer(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        btime=datetime.now()
        dift=datetime.now()-btime
        print('%s %s' % (func.__name__ , dift))
        return func(*args, **kw)
    return wrapper
# 初始化
@betimer
def init():
    '''
    @note:初始化函数,生成对应文件夹
    '''
    w.start()
    for path in ['raw','fig','data','daily','result']:
        if not os.path.exists(f'../{path}'):
            os.mkdir(f'../{path}')
@betimer
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
    today=datetime.today()
    a=w.wsd(ctr, "close,volume,amt,oi,settle", "2008-01-01", f"{today.year}-{today.month}-{today.day}", "")#收盘 成交 总量 持仓 结算
    df=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times).T # 转换成pd格式
    df.to_csv(f"../raw/{ctr}.csv") #存储到本地
#    df=pd.DataFrame.from_csv(f"../raw/{ctr}.csv")#测试时使用
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

@betimer
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
    
def get_ratio(sym):
    '''
    @note:提取品种保证金数据
    '''
    global ratio
    return ratio[str.upper(sym)]

def fix_mtpr(sym):
    '''
    @note:对合约乘数变化过的品种乘数进行处理，方法为：在变化时间段内按照线性变化做平滑处理
    '''
    global sym_index
    global mtpr
    if type(mtpr[sym])!=type(1.0):
        return
    idx=sym_index[sym]
    tmp_mtpr=pd.DataFrame([mtpr[sym] for x in range(0,len(idx))],index=idx)
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
        roll(tmp_mtpr,"2011-01-03","2011-11-30",10,50)
        roll(tmp_mtpr,"2011-11-30",idx[-1],50,50)
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
    mtpr[sym]=tmp_mtpr.copy()
        
def fix_ratio(sym):
    '''
    @note:对合约保证金乘数变化过的品种乘数进行处理，方法为：在变化时间段内按照线性变化做平滑处理
    '''
    global sym_index
    global ratio
    if type(ratio[sym])!=type(1.0):
        return
    idx=sym_index[sym]
    tmp_ratio=pd.DataFrame([ratio[sym] for x in range(0,len(idx))],index=idx)
    if sym in ['IF','IH']:
        roll(tmp_ratio,idx[0],"2015-08-25",.10,.10)
        roll(tmp_ratio,"2015-08-26","2015-08-31",.10,.20)
        roll(tmp_ratio,"2015-08-31","2015-09-06",.20,.20)
        roll(tmp_ratio,"2015-09-06","2015-09-07",.20,.30)
        roll(tmp_ratio,"2015-09-07","2017-02-17",.30,.30)
        roll(tmp_ratio,"2017-02-17",idx[-1],.20,.20) 
    if sym=='IC':
        roll(tmp_ratio,idx[0],"2015-08-25",10,10)
        roll(tmp_ratio,"2015-08-26","2015-08-31",.10,.20)
        roll(tmp_ratio,"2015-08-31","2015-09-06",.20,.20)
        roll(tmp_ratio,"2015-09-06","2015-09-07",.20,.30)
        roll(tmp_ratio,"2015-09-07","2017-02-17",.30,.30)
        roll(tmp_ratio,"2017-02-17",idx[-1],.25,.25)
    ratio[sym]=tmp_ratio.copy()


@betimer
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

@betimer
def download_all(): 
    '''
    @note:下载所有品种的量价数据 
    '''
    for ctr in getctrs():
        sym=re.search('(\D+)',ctr).group(0)
        download(ctr,sym)
    
@betimer
def trade(sym,ctrs): 
    '''
    @note:合并单品种的成交量
    只有中金所是单边计算 其余均为双边计算
    '''
    global persym
    df=pd.concat([ctr['VOLUME']*ctr['SETTLE']*get_mtpr(sym)[0] for ctr in ctrs.values()],axis=1)
    if sym not in ['IF','IH','IC','TF','T']: #只有中金所是单边计算 其余均为双边计算
        df=df/2
    persym[sym]=df.sum(1) #按日合并数据
    
@betimer
def position(sym,ctrs):
    '''
    @note:合并单品种的持仓额
    '''
    global persym
    df=pd.concat([ctr['SETTLE']*ctr['OI']*get_mtpr(sym)[0] for ctr in ctrs.values()],axis=1)
    if sym not in ['IF','IH','IC','TF','T']: #只有中金所是单边计算 其余均为双边计算
        df=df/2
    persym[sym]=df.sum(1) #按日合并数据
    
@betimer
def margin(sym,ctrs):
    '''
    @note:按保证金计算持仓数据,合并单品种的持仓保证金以及每日持仓保证金
    '''
    global persym
    df=pd.concat([ctr['OI']*ctr['SETTLE']*get_mtpr(sym)[0]*get_ratio(sym)[0] for ctr in ctrs.values()],axis=1)
    if sym not in ['IF','IH','IC','TF','T']: #只有中金所是单边计算 其余均为双边计算
        df=df/2
    persym[sym]=df.sum(1) #按日合并数据    
@betimer
def merge(f):
    '''
    @note:合成三种分类数据
    '''
    global persym;persym=dict()
    name=getattr(f,'__name__')
    for sym in ctrs_data.keys():
        fix_mtpr(sym)
        fix_ratio(sym)
        f(sym,ctrs_data[sym])
    equity=0
    for sym in ['IF','IH','IC']:
        equity=equity+persym[sym] 
    fix=0
    for sym in ['TF','T']:
        fix=fix+persym[sym]
    allpart=0
    for sym in persym.keys():
        allpart=allpart+persym[sym] 
    comm=allpart-equity-fix
    p=pd.concat([allpart,comm,equity,fix],axis=1)
    p.columns=['ALL',"commodity","equity","bond"]
    p.to_csv(f"../data/{name}.csv")
    p=pd.concat(persym.values(),axis=1)
    p.columns=persym.keys()
    p.to_csv(f"../data/{name}_detail.csv")
    

init() 
download_all()
load_mtpr()
for f in [margin,position,trade]:
    merge(f)


#if __name__=="__main__":
#    import download
#    print(help(download))
    