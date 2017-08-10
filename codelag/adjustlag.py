#-*- coding: utf-8 -*-
"""
公司：中融汇信
创建时间：2017/07/31
目的： 用来把差分的日频预测数据加上一个月真实客户权益金数据，得到最终预测值。
"""

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
global real
def loadcsv(filename):
    re=pd.read_csv(filename,index_col=0)
    re.index=[pd.Timestamp(x[0:10]) for x in re.index]
    re.index=[datetime(x.year,x.month,x.day) for x in re.index] 
    return re
#spes=['com','equ','fix']
spes=['com']
real=loadcsv(f"../data/marpart.csv")   
for spe in spes:
    real=pd.DataFrame(real[f"mar_{spe}"]) 
    predict=loadcsv(f"../daily/{spe}_6_2_0.csv")  #已经选好的模型预测结果
    predict.columns=[f"{spe}_6_2_0"]
    predict[f'real_{spe}']=0
    predict[f'predict']=0
    for day1 in predict.index:
        for day2 in real.index:
            if (day1.month==(day2.month+1) and day1.year==day2.year):
                predict.loc[day1,[f'real_{spe}']]=float(real.loc[day2,[f"mar_{spe}"]])
            elif (day1.month==1 and day1.year==(day2.year-1)):
                predict.loc[day1,[f'real_{spe}']]=float(real.loc[day2,[f"mar_{spe}"]])
    predict['predict']=predict[f'real_{spe}']+predict[f"{spe}_6_2_0"]
    predict.to_csv(f'../result/{spe}_predict_result.csv')
    
    

            
    