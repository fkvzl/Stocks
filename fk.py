# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 10:49:19 2021

@author: fkvzl
"""

import tushare as ts

pro = ts.pro_api('ebe4734e785004ada3e0f4e03da59a5dee8c7da0b7820ce5c50fb30e')



def myMACD(price, fastperiod, slowperiod, signalperiod):
    ewma12 = price.ewm(span=fastperiod,adjust=False).mean()
    ewma60 = price.ewm(span=slowperiod,adjust=False).mean()
    dif = ewma12-ewma60
    dea =  dif.ewm(span=signalperiod,adjust=False).mean()
    bar = (dif-dea)*2 #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar



def cal_macd_system(data):
    '''
    data是包含高开低收成交量的标准dataframe
    short_,long_,m分别是macd的三个参数
    返回值是包含原始数据和diff,dea,macd三个列的dataframe
    '''
    data['EMA12'] = data['close'].ewm(alpha=2 / 13, adjust=False).mean() 
    data['EMA26'] = data['close'].ewm(alpha=2 / 27, adjust=False).mean()
    
    data['DIFF'] = data['EMA12'] - data['EMA26']
    data['DEA'] = data['DIFF'].ewm(alpha=2 / 10, adjust=False).mean()
    data['MACD'] = 2 * (data['DIFF'] - data['DEA'])
    return data['DIFF'], data['DEA'],data['MACD']
 

def get_cyb():
    stocks = pro.stock_basic()
    cyb = stocks[stocks['ts_code'].str.contains('^300')]
    return cyb['ts_code'].values

def macdhist_300(days):  #最近10天用-10参数
    stocks = pro.stock_basic()
    cy_stock = stocks[stocks['ts_code'].str.contains('^30')]
 
    for stock in cy_stock['ts_code'].values: #获取全量股票
        try:
            df = pro.daily(ts_code=stock)#遍历每天行情
            df=df[::-1]  #倒序，同sort区别为sort为排序方式
            dif,dea,hist=myMACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
            hist = hist.values[days:]
            if  (len(hist [ (hist >=-0.07) * (hist <= 0.07)]))>=80 :
                print(stock)
        except:
            print('不可用：',stock)
 

# df=pro.daily(ts_code='300001.SZ')
# df=df[::-1]
# dif,dea,hist=myMACD(df['close'],12,26,9)
# hist = hist.values[-10:]
# print(len(hist [ (hist >=-0.07) * (hist <= 0.07)]))

"""
获取创业板df函数
for i in get_cyb():
    print(i)
"""