# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 09:20:12 2017

@author: Lori
"""
import pandas as pd
import re
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib as mpl
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY,YEARLY
def loadcsv(filename):
    re=pd.read_csv(filename,index_col=0)
    re.index=[pd.Timestamp(x[0:10]) for x in re.index]
    re.index=[datetime(x.year,x.month,x.day) for x in re.index] 
    return re
 
d=loadcsv('../data/wind_index.csv')#读入wind商品指数日频数据
d['equity_index'].plot(legend='equity_index',title='compare result',figsize=(24,12))
plt.ylabel('price')
d['fix_index'].plot(secondary_y=True,legend='fix_index',figsize=(24,12))
plt.plot()
plt.grid()
plt.savefig('../fig/daily.png')  
