# -*- coding: utf-8 -*-
"""
公司：中融汇信
作者：王德扬
创建时间：2017/07/19
目的： 将文件按照中文备份保存
"""
# 生成中文文件
import shutil
p={"commodity_position":"商品持仓金额",
"commodity_pre":"商品持仓保证金额",
"commodity_trade":"商品成交金额",
"deposit":"金融机构：各项存款余额",
"equity_position":"权益持仓金额",
"equity_pre":"权益持仓保证金额",
"equity_trade":"权益成交金额",
"fix_position":"固收持仓金额",
"fix_pre":"固收持仓保证金额",
"fix_trade":"固收成交金额",
"margin":"客户权益金",
"nobank":"非存款金融机构存贷款",
"position":"各品种持仓金额",
"positionall":"总持仓金额",
"position_margin":"总持仓保证金",
"margin_m":"总持仓保证金_月",
"settlement":"证券结算资金数据",
"trade":"各品种成交金额",
"tradeall":"总成交金额"}

for name in p.keys():
    shutil.copy("../data/"+name+".csv","../data/"+p[name]+".csv")
    
#if __name__=="__main__":
#    import name
#    print(help(name))