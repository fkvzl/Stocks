# -*- coding: utf-8 -*-
"""
Created on Thu May 13 08:06:11 2021

@author: fkvzl

E-mail:fkvzl@qq.com

主题：数字可视化
思路：各市场每日涨跌数量、各板块涨跌数量

"""
import xcsc_tushare as ts
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
#初始化
ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')


#横坐标x：交易日期
tra_cal = pro.trade_cal(start_date=20210101,end_date=20210519)
x = tra_cal.trade_date.values

#纵坐标：每天的涨跌数量
#yr = []
#yf = []
#for i in x:
#    df=pro.daily(trade_date=i)
#    dfcyb_r=df[df.ts_code.str.contains('^300')& df.pct_chg>0]
#    dfcyb_f=df[df.ts_code.str.contains('^300')& df.pct_chg<0]
#    cyb_rises=dfcyb_r['pct_chg'].count()
#    cyb_fails=dfcyb_f['pct_chg'].count()
#    yr.append(cyb_rises)   
#    yf.append(cyb_fails)

dataf = {'A':['20210101','20210102','20210103'],
        'B':['10','20','6'],
        'C':['15','5','19']}
df = pd.DataFrame(dataf)
 
##画图
plt.figure()
plt.plot(df.A,df.C)
plt.show()
