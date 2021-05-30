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


#下载交易日期
# df_cal = pro.trade_cal(start_date=20210101,end_date=20210519)
# df_cal.to_excel('D:/tra_date.xlsx')  

#结果集定义
df_date = pd.read_excel('D:/tra_date.xlsx')
#获取日期
dates = df_date.trade_date.values

###主函数
for i in dates:
    #获取每天创业板的涨跌数量
    df=pro.daily(trade_date=str(i))
    df_300 = df[df.ts_code.str.contains('^300')]
    up_300 = df_300[df_300.pct_chg>0].pct_chg.count()
    down_300 = df_300[df_300.pct_chg<0].pct_chg.count()
    
 
    
    #复制涨跌数量到结果集里
    df_date.loc[df_date[df_date.trade_date==i].index,'up']=up_300
    df_date.loc[df_date[df_date.trade_date==i].index,'down']=down_300

df_date.to_excel('D:/tra_date.xlsx') 
###主函数


##画图
plt.figure()
plt.plot(df_date.trade_date,df_date.up)
plt.tight_layout()
plt.show()
##主函数