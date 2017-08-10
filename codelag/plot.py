# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:33:26 2017

@author: Lori
"""
      
import numpy as np  
import matplotlib as mpl  
import matplotlib.pyplot as plt  
import pandas as pd
from datetime import datetime 

def loadcsv(filename):
    re=pd.read_csv(filename,index_col=0)
    re.index=[pd.Timestamp(x[0:10]) for x in re.index]
    re.index=[datetime(x.year,x.month,x.day) for x in re.index] 
    return re

d=loadcsv('../data/wind_index.csv')#读入wind商品指数日频数据

fig = plt.figure()       
start =datetime(2013,1,1)  
end = datetime(2017,6,1)
#start =datetime(d.index[1].year,d.index[1].month,d.index[1].day)  
#end = datetime(d.index[-1].year,d.index[-1].month,d.index[-1].day)
# 设置日期的间隔为1  
delta = datetime.timedelta(days= 1)       
# 生成一个matplotlib可以识别的日期对象  
dates = mpl.dates.drange(start, end, delta)  
# y轴产生随机数  
y = d['equity_index']  
      
# 获取当前的坐标  
ax = plt.gca()  
# 使用plot_date绘制日期图像  
ax.plot_date(dates, y, linestyle = "-", marker = ".")  
  
# 设置日期的显示格式  
date_format = mpl.dates.DateFormatter("%Y-%m-%d")  
ax.xaxis.set_major_formatter(date_format)  
      
# 日期的排列根据图像的大小自适应  
fig.autofmt_xdate()  
      
plt.show()  