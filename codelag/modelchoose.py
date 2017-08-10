# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/31
目的： 输出模型比较结果,计算结果保存至modelchoose中
"""
import pandas as pd
import numpy as np
from datetime import datetime


global pdt
global real


#spes=['com']
spes=['com','equ','fix']
real=dict()
pdt=dict()
diff=dict()

def load_real(spe):
    '''
    @note:读入分大类客户权益金真实数据（月频），返回差分数据
    '''
    a=pd.read_csv("../data/marpart.csv",index_col=0)    
    a=pd.DataFrame(a["mar_"+spe])
    a.index=[pd.Timestamp(x) for x in a.index]
    a.index=[datetime(x.year,x.month,1) for x in a.index]
    a=pd.DataFrame(a.diff(periods=1,axis=0))
    return a

def load_pdt(name):
    '''
    @note:读入具体（大类，模型是否有截距项，估计滞后阶数，回归窗宽）客户权益金预测数据（日频），然后月频数据
    '''
    b=pd.read_csv(f"../daily/{name}.csv",index_col=0)
    b.index=[pd.Timestamp(x) for x in b.index]
    b=b.resample('M').mean()
    b.index=[datetime(x.year,x.month,1) for x in b.index]
    return b
pl=""
for spe in spes:
    real[spe]=load_real(spe)
    for cst in [0,1]:
        for lag in [1,2]:
            for win_w in [6,12,18,24]:
                name=f"{spe}_{win_w}_{lag}_{cst}"
                pdt[name]=load_pdt(name)
#                print(pdt[name])
                d=pd.concat([pdt[name],real[spe]],axis=1)
                diff[name]=d['0']-d[f"mar_{spe}"]
#                diff[name]=pdt[name]-real[spe]        #这个上周是可以的
#                diff[name]=pdt.iloc[:,[0]]-real.iloc[:,[0]]
#                print(pdt[name])
                nv=diff[name].dropna(how="any")
                #print("##1",nv,"##1")
#                nv=np.array(nv[nv.columns[0]])
                std=nv.std()
                mean=nv.mean()
                pl=pl+f"{name},{std},{mean}\n"
                print("##2",name,",",std,",",mean,"##2")#
                data=pd.concat([real[spe],pdt[name],diff[name]],axis=1).dropna(how='any')
                data.to_csv(f"../result/{name}.csv",header=("real","predict","diff"))#
pl=pl.replace('_',",")
with open('../result/result.all.csv',"w") as f:
    f.write(pl)

'''
@note:对大类选择最合适的模型，模型比较方法：通过预测值与实际值作差的均值和方差作为衡量标准
'''
#for spe in spes:
#    real[spe]=load_real(spe)
#    print(real[spe])
#    for cst in [0]:
#        for lag in [1]:
#            for spe in spes:
#                for win_w in [6]:
#                    name=f"{spe}_{win_w}_{lag}_{cst}"
#                    pdt[name]=load_pdt(name)
#                    print(pdt[name])
#                    diff[name]=pdt[name]-real[spe]
#                    print(type(pdt[name]),type(real[spe]))
#                    print(diff[name])
#                    nv=diff[name].dropna(how="any")
##                    print(nv)
#                    nv=np.array(nv[nv.columns[0]])
#                    std=nv.std()
#                    mean=nv.mean()                  
#                    print(name,",",std,",",mean)