# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 13:12:06 2021

@author: Administrator
"""

import xcsc_tushare as ts
import talib as tl
from sqlalchemy import create_engine
import pymysql
import numpy as np
import matplotlib.pyplot   as plt
import pandas  as pd



ip='127.0.0.1'
user='stock'
pwd='stock'
db='stockdb'
engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{ip}:3306/{db}')


import numpy as np
def kdj():
    stock='002594.SZ'
    query_sql='''select * from stdaily where ts_code=?''',(stock)
    
    df=pd.read_sql_query(query_sql,engine)
    #df.reverse()
    print(df)

kdj_position=pd.Series([False,True,True,False])
qqshift=pd.Series([1,2,3,4,5]).shift()
print(qqshift)


df.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
print((kdj_position == True) & (kdj_position.shift() == False))
print(kdj_positon)