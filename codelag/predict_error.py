 #-*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/31
目的： 选择预测客户权益金数据的模型，回归预测使用一阶差分数据，结果保存在daily中
"""
#先将滞后期确定，向前取N个月的数据，按照回归窗宽t从后向前取t个可用数据做回归。
import pandas as pd
import numpy as np
import time
from datetime import datetime
from datetime import timedelta
import statsmodels.api as sm

global mod;mod=dict()

'''
@note:读入数据，按保证金种类占比将客户权益金分类
'''
#def log(func):
#    def wrapper(*args, **kw):
#        print('call %s():' % func.__name__)
#        print(com_m.columns)
#        return func(*args, **kw)
#    return wrapper

data=pd.read_csv('../data/margin.csv',index_col=0)
da=pd.read_csv('../data/margin_compare.csv',index_col=0)
today = time.strftime('%Y-%m-%d',time.localtime())
#day=datetime.date.today() 
#day=day+pd.timedelta(days=1)
now = datetime.now() 
today=now

##把变量放到dict中 
dd=dict()  ##日频分品种的持仓保证金
dc=dict()  ##月频分品种的持仓保证金
dm=dict()  ##月频分品种的客户权益金

for i,name in enumerate(['pos','com','equ','fix']):
    dd[name]=data.iloc[:,i:i+1]
    dd[name].index=[pd.Timestamp(x) for x in dd[name].index]
    dc[name+"_m"]=da.iloc[:,i:i+1]
    dc[name+"_m"].index=[pd.Timestamp(x) for x in dc[name+"_m"].index]
mar=da.iloc[:,4:5]  ##客户权益金真实数据
mar.index=[pd.Timestamp(x) for x in mar.index]

for name in ('com','equ','fix'):
    dc[name+"_m"].columns=['a']
    dm[name]=mar.marginreal*dc[name+"_m"].a/dc["pos_m"].ALL
    dc[name+"_m"].columns=[name+"_m"]
    dm[name]=pd.DataFrame(dm[name])
    dm[name].columns=["mar_"+name]
    dm[name].index=[pd.Timestamp(x) for x in dm[name].index]
    
b=pd.DataFrame()
for name in dm:
    c=pd.DataFrame(dm[name])
    b=pd.concat([b,c],axis=1)
b.columns=["mar_com","mar_equ","mar_fix"]
b.to_csv(f"../data/marpart.csv")

def backmonth(y,m,k):
    '''
    @note:按照滞后与窗宽返回前后调整月份
    '''
    while(m-k<=0):
        y=y-1
        m=m+12
    while(m-k>12):
        y=y+1
        m=m-12
    return y,m-k
#@log
def getX(lag,spe,win_w,t):
    '''
    @note:提取分类保证金数据,返回差分时间序列
    example:
        2016.12.01   100
        2017.01.01   200
    diff:
        2017.01.01   200-100=100
    '''
    data=dc[spe+"_m"]
    st=datetime(*backmonth(t.year,t.month,win_w+lag-1),1)
    et=datetime(*backmonth(t.year,t.month,lag),1)
    data=data.diff(periods=1, axis=0)
    data=data[st:et]
#    print("st\n",st,"et\n",et)
#    print(data,'#########')
    data=data.dropna(how="any")
#    print(data)
    return data

#@log
def getY(lag,spe,win_w,t):
    '''
    @note:提取分类客户权益金数据,返回差分时间序列
    '''
    data=dm[spe]   
    st=datetime(*backmonth(t.year,t.month,win_w+lag-1),1)
    et=datetime(*backmonth(t.year,t.month,lag),1)
    data=data.diff(periods=1, axis=0)    
    data=data[st:et]
    data=data.dropna(how="any")
#    print(data,'#########')
    return data

#@log
def getx(spe,t):
    '''
    @note:提取预测的保证金日频差分数据
    rolling:向前Window天取平均
    diff：data(t)-data(t-1)
    '''
    data=dd[spe]
#    print(data[data.index==t].iloc[0,0],"******")
    data=data.rolling(window=3).mean()
#    print(data[data.index==t].iloc[0,0],"******")
    data=data.diff(periods=1,axis=0)
#    print(data[data.index==t].iloc[0,0],"******")
    return data[data.index==t].iloc[0,0]

#@log    
def ols(X,Y,x,cst):
    '''
    @note:对X,Y做线性回归，并得到预测值
    @X:保证金月频数据
    @Y:客户权益金月频数据
    @x:输入保证金日频数据求预测值
    @constant：是否有截距项
    ''' 
    global mod
    [X,Y,x]=[np.array(i) for i in [X,Y,x]]
    if cst==True:
        X=sm.add_constant(X)
        x=np.hstack(([1],x))
    model=sm.OLS(Y,X)
    mod=model
    results=model.fit()
#    print(results.params)
    return [float(model.predict(results.params,x))]    
#@log                
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
#    print(Xuse,"\n\n",Yuse,"\n\n",xuse)
    predict=ols(Xuse,Yuse,xuse,cst)
    return predict
#@log
def start(win_w,lag,spe):
    '''
    @note:客户权益金预测起始时间
    '''
    t=datetime(*backmonth(2013,3,-1*(win_w+lag-1)),1)
    if spe=='fix':
        t=datetime(*backmonth(2013,9,-1*(win_w+lag-1)),1)
    return pd.to_datetime(t)
#@log    
def datelist(win_w,lag,spe):
    '''
    @note:客户权益金预测时间范围
    '''     
    tm=start(win_w,lag,spe) #转换成时间  
    et=datetime.now()+timedelta(days=1)  
    t=dd['com'][tm:et]
    return t.index

result=dict()
for cst in [0,1]:
    for lag in [1,2]:
        for spe in ['com','equ','fix']:
            for win_w in [6,12,18,24]:
                name=f"{spe}_{win_w}_{lag}_{cst}"
#                print(name)
                result[name]=dict()
                for t in datelist(win_w,lag,spe):
                    result[name][t]=[*pre(cst,lag,spe,win_w,t)]     
#result=dict()
#global cst
#global lag
#global spe
#global win_w
#global t
#for cst in [1]:
#    for lag in [1]:
#        for spe in ['com']:
#            for win_w in [6]:
#                name=f"{spe}_{win_w}_{lag}_{cst}"
#                result[name]=dict()
#                for t in [pd.Timestamp("2017-06-05 00:00:00.005000")]:
#                    result[name][t]=[*pre(cst,lag,spe,win_w,t)]
#                    print(t,result[name][t])


global a
# daily:差分预测的日频客户权益金结果
for name in result:
    a=pd.DataFrame(result[name]).T
    a.to_csv(f"../daily/{name}.csv")
   
#print(pre("fix",24,2,0,))
#kk=result["com_12_1_0"]
#ss=pd.DataFrame(kk).T