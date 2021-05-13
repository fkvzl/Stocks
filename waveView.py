# -*- coding: utf-8 -*-
"""
Created on Sun May  9 11:54:31 2021

@author: fkvzl

E-mail: fkvzl@qq.com

Tel: 15257442134
"""



import xcsc_tushare as ts
ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')



#获取每日涨跌数量，横轴日期，绘制曲线
df_s = pro.stock_basic(exchange='SSE')
#df_s = df_s[df_s.ts_code.str.contains('^60')]
#print (df_s)
df = pro.daily(ts_code='600001.SH',trade_date='20210507')
df = df[df.ts_code.str.                                                                                                                                                     ]
print(sum(df['pct_chg']<0))