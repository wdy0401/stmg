# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/21
目的：线性回归
"""


import os
import re
import pandas as pd
from datetime import datetime

'''
运用一组数据模拟
a为月度汇总数据
'''

a=pd.read_csv('../data/margin_m.csv',names=['margin_m'])
a.index=[pd.Timestamp(x) for x in a.index]
b=pd.DataFrame([2],index=['a'])