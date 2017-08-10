# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/31
修改时间：2017/08/02
目的： 输出品种最优模型预测的客户权益金与真实值的差分比较图
"""
'''

'''
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
global real
def loadcsv(filename):
    re=pd.read_csv(filename,index_col=0)
    re.index=[pd.Timestamp(x[0:10]) for x in re.index]
    re.index=[datetime(x.year,x.month,x.day) for x in re.index] 
    return re
    
spes=['com','equ','fix']
for spe in spes:
    global real
    predict=loadcsv(f"../daily/{spe}_6_2_0.csv")  
    real=loadcsv(f"../result/{spe}_6_2_0.csv")  
    #real.loc[nextmonth]={'real':0,'predict':0,'diff':0}
    total=pd.concat([predict,real],axis=1)
#    print(total)
    total=total.fillna(method='pad')
#    print(total)
    total.to_csv('../result/zx.csv')
    total.columns=['predict value','true value month','predict value month','predict error']
    total=total.drop('predict error',1)
    total.to_csv("../result/total.csv")
    total.plot(figsize=(24, 12))
#    total.plot()
    plt.savefig(f"../fig/fig_{spe}.png")