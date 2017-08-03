 #-*- coding: utf-8 -*-
"""
Created on Tue Jul 25 13:46:59 2017

@author: Lori
"""
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import statsmodels.api as sm

def backmonth(y,m,k):
    while(m-k<=0):
        y=y-1
        m=m+12
    return y,m-k
def getX(lag,spe,win_w,t):
    '''
    @note:提取分类保证金数据
    '''
    if  spe=='com':
        data=com_m
    elif spe=='equ':
        data=equ_m
    elif spe=='fix':
        data=fix_m
    st=datetime(*backmonth(t.year,t.month,win_w+lag-1),1)
    et=datetime(*backmonth(t.year,t.month,win_w+lag),1)
    data=data[st:et]
    return data[data>0].dropna(how="any")

def getY(lag,spe,win_w,t):
    '''
    @note:提取分类客户权益金数据
    '''
    if  spe=='com':
        data=mar_com
    elif spe=='equ':
        data=mar_equ
    elif spe=='fix':
        data=mar_fix
    st=datetime(*backmonth(t.year,t.month,win_w+lag-1),1)
    et=datetime(*backmonth(t.year,t.month,win_w+lag),1)
    data=data[st:et]
    return data[data>0].dropna(how="any")
def getx(spe,t):
    '''
    @note:提取预测的保证金日频数据
    '''
    if  spe=='com':
        data=com
    elif spe=='equ':
        data=equ
    elif spe=='fix':
        data=fix
    return data[data.index==t].iloc[0,0]
    
def ols(X,Y,x,cst):
    '''
    @note:对X,Y做线性回归，并得到预测值
    @X:保证金月频数据
    @Y:客户权益金月频数据
    @x:输入保证金日频数据求预测值
    @constant：是否有截距项
    '''
    
    X=np.array(X)
    Y=np.array(Y)
    x=np.array(x)
    
#    print("Ysize,Xsize 2",Y.size,X.size)
    if cst==True:
        X=sm.add_constant(X)
        x=np.hstack(([1],x))
        
  
#    print("Ysize,Xsize 3",Y.size,X.size)
#    print(cst, lag, spe, win_w, t)
    model=sm.OLS(Y,X)
    results=model.fit()
    return [float(model.predict(results.params,x))]    
           
pos=pd.read_csv('../data/position_margin.csv',names=['position_margin'])
pos.index=[pd.Timestamp(x) for x in pos.index]
pos_m=pos.resample('M').mean()
pos_m.index=[datetime(x.year,x.month,1) for x in pos_m.index]

mar=pd.read_csv('../data/margin.csv',names=['margin'])
mar.index=[pd.Timestamp(x) for x in mar.index]
mar.index=[datetime(x.year,x.month,1) for x in mar.index]
mar_m=mar.resample('M').mean()
mar_m.index=[datetime(x.year,x.month,1) for x in mar_m.index]

com=pd.read_csv('../data/commodity_pre.csv',names=['commodity_pre'])
com.index=[pd.Timestamp(x) for x in com.index]
com_m=com.resample('M').mean()
com_m.index=[datetime(x.year,x.month,1) for x in com_m.index]

equ=pd.read_csv('../data/equity_pre.csv',names=['equity_pre'])
equ.index=[pd.Timestamp(x) for x in equ.index]
equ_m=equ.resample('M').mean()
equ_m.index=[datetime(x.year,x.month,1) for x in equ_m.index]

fix=pd.read_csv('../data/fix_pre.csv',names=['fix_pre'])
fix.index=[pd.Timestamp(x) for x in fix.index]
fix_m=fix.resample('M').mean()
fix_m.index=[datetime(x.year,x.month,1) for x in fix_m.index]
    
mar_com=com_m.commodity_pre/pos_m.position_margin*mar_m.margin
mar_com.index=com_m.index
mar_com=pd.DataFrame(mar_com)
mar_equ=equ_m.equity_pre/pos_m.position_margin*mar_m.margin
mar_equ.index=com_m.index
mar_equ=pd.DataFrame(mar_equ)
mar_fix=fix_m.fix_pre/pos_m.position_margin*mar_m.margin
mar_fix.index=com_m.index
mar_fix=pd.DataFrame(mar_fix)

def pre(cst,lag,spe,win_w,t):
    '''
    @note:求日频客户权益金预测值
    @constant：截距项
    @lag：一两个月
    @species：商品股指固收
    @window_width：窗宽 t时间点
    '''
    Xuse=getX(lag,spe,win_w,t)
    Yuse=getY(lag,spe,win_w,t)

    xuse=getx(spe,t)
#    print("X",Xuse,"\ny",Yuse,"\nx",xuse)
#    print("Ysize,Xsize ",Yuse.size,Xuse.size)
    predict=ols(Xuse,Yuse,xuse,cst)
#    print('predict',predict)

    return predict

def start(win_w,lag,spe):
    '''
    @note:客户权益金预测起始时间
    '''
    t=datetime(2013,1,1)+timedelta((win_w+lag-1)*31)
    if spe=='fix':
        t=datetime(2013,9,1)+timedelta((win_w+lag-1)*31)
    t=datetime(t.year,t.month,1)
    return pd.to_datetime(t)
    
def datelist(win_w,lag,spe):
    '''
    @note:客户权益金预测时间范围
    ''' 
    
    tm=start(win_w,lag,spe)#转换成时间  
    et=pd.to_datetime(datetime(com.index[-1].year,com.index[-1].month,1))
    time=com[tm:et]#d 需要检查+-1
    return time.index

result=dict()
global cst
global lag
global spe
global win_w
global t
for cst in [0,1]:
    for lag in [1,2]:
        for spe in ['com','equ','fix']:
            for win_w in [6,12,18,24]:
                name=f"{spe}_{win_w}_{lag}_{cst}"
                result[name]=dict()
                for t in datelist(win_w,lag,spe):
                    result[name][t]=[*pre(cst,lag,spe,win_w,t)]     
#result=dict()
#global cst
#global lag
#global spe
#global win_w
#global t
#for cst in [0,1]:
#    for lag in [1]:
#        for spe in ['com']:
#            for win_w in [6]:
#                name=f"{spe}_{win_w}_{lag}_{cst}"
#                result[name]=dict()
#                for t in [pd.Timestamp("2015-01-05 00:00:00.005000")]:
#                    result[name][t]=[*pre(cst,lag,spe,win_w,t)]                    


global a
for name in result:
    
#    print(result[name])
    print(name)
    a=pd.DataFrame(result[name])
#    break
    a.to_csv(f"../result/{name}.csv")     
    
#print(pre("fix",24,2,0,))
#kk=result["com_12_1_0"]
#ss=pd.DataFrame(kk).T