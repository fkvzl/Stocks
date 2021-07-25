# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:23:10 2021

@author: Administrator
"""
import xcsc_tushare as ts
from sqlalchemy import create_engine
import pymysql
import numpy as np
import matplotlib.pyplot   as plt
import pandas  as pd
import xlrd

ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')



ip='127.0.0.1'
user='stock'
pwd='stock'
db='stockdb'
engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{ip}:3306/{db}')




'''
1、talib的macd存在前33个null，自用macd已优化
2、使用时，整体周期取股票从发行以来（涉及递归，不支持取中间某段）
'''
def myMACD(price, fastperiod, slowperiod, signalperiod):
    ewma12 = price.ewm(span=fastperiod,adjust=False).mean()
    ewma60 = price.ewm(span=slowperiod,adjust=False).mean()
    dif = ewma12-ewma60
    dea =  dif.ewm(span=signalperiod,adjust=False).mean()
    bar = (dif-dea)*2 #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar


def myKDJ(low,high,close):
    low_list = low.rolling(9, min_periods=9).min()
    low_list.fillna(value = low.expanding().min(), inplace = True)
    high_list = high.rolling(9, min_periods=9).max()
    high_list.fillna(value = high.expanding().max(), inplace = True)
    rsv = (close - low_list) / (high_list - low_list) * 100

    df['K'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    kdj_position=df['K']>df['D']   #k->d-0+金叉；k->d->0-死叉
    
    df.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
    df.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'
    print(df)
    


'''
日线kdj
    1金叉：
    2死叉：
60分时kdj
    3金叉：
    4死叉：
'''
def kdj():
    global df
    df=pro.daily(ts_code='300905.SZ')
    df=df[::-1]
    myKDJ(df['low'],df['high'],df['close'])
    

 


 



    
    
    
'''
1、vr有多次冲高,底部抬高——》意图明显
def vr():
'''

    
    
    
    
    
    
'''
1创业板300+零轴up+零轴down+下限
2满足macd多
390天最低kdj
'''
def macdhist_300(days):
    stocks = pro.stock_basic()
    cy_stock = stocks[stocks['ts_code'].str.contains('^30')]
    stocklist=[]
    for stock in cy_stock['ts_code'].values: #获取全量股票
        try:
            df = pro.daily(ts_code=stock)#遍历每天行情
            df=df[::-1]  #倒序，同sort区别为sort为排序方式
            dif,dea,hist=myMACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
            hist = hist.values[days:]
            if  (len(hist [ (hist >=-0.07) * (hist <= 0.07)]))>=22:
                stocklist.append(stock)
        except:
            print('不可用：',stock)
    return stocklist


macdhist_300(30)
