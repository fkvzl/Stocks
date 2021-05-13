# -*- coding: utf-8 -*-
"""
Created on Thu May 13 08:06:11 2021

@author: fkvzl

E-mail:fkvzl@qq.com

主题：数字可视化
思路：各市场每日涨跌数量、各板块涨跌数量

"""
import xcsc_tushare as ts

ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')
df=pro.daily(trade_date=20210512)
df_cyb=df[df['ts_code'].str.contains('^300')]
cyb_rises=(df_cyb[df_cyb['pct_chg']>0].count())
cyb_fails=(df_cyb[df_cyb['pct_chg']<0].count())
print(flat)