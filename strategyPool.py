# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:23:10 2021

@author: Administrator
"""
import xcsc_tushare as ts
import talib as tl
from sqlalchemy import create_engine
import pymysql
import numpy as np
import matplotlib.pyplot   as plt
import pandas  as pd


ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')



ip='127.0.0.1'
user='stock'
pwd='stock'
db='stockdb'
engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{ip}:3306/{db}')


#指标
def myMACD(price, fastperiod, slowperiod, signalperiod):
    ewma12 = price.ewm(span=fastperiod,adjust=False).mean()
    ewma60 = price.ewm(span=slowperiod,adjust=False).mean()
    dif = ewma12-ewma60
    dea =  dif.ewm(span=signalperiod,adjust=False).mean()
    bar = (dif-dea)*2 #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar


#选股
#hist在1.21开始没跌破0
#def getLongLow(price,sday,eday):
    #设置开始、截止时间
    #设置下跌幅度
    #筛选发生过满足以上条件的股票，观察走势，比如价格低于17年，macd是红的超过了1个月
    

df = pro.daily(ts_code='002269.SZ')#遍历每天行情
df=df[::-1]  #倒序，同sort区别为sort为排序方式

#以下两种方式效果一致，talib无前33位，区域需要全周期
#dif,dea,hist=myMACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
dif,dea,hist=tl.MACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)


hist = hist*2
print(hist)