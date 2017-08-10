# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/19
目的： 将文件按照中文备份保存
"""
# 生成中文文件
import shutil
p={"margin.csv":"持仓保证金额",
"marginreal.csv":"客户权益金月频数据",
"margin_compare.csv":"持仓保证金与客户权益金月频数据",
"margin_detail.csv":"分品种持仓保证金额",
"position.csv":"持仓金额",
"position_detail.csv":"分品种持仓金额",
"trade.csv":"成交金额",
"trade_detail.csv":"分品种成交金额"}

for name in p.keys():
    shutil.copy("../data/"+name,"../data/"+p[name]+".csv")
    
#if __name__=="__main__":
#    import name
#    print(help(name))