# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 22:09:25 2021

@author: fkvzl
"""
import pandas as pd
 
df_codes = pd.read_excel('C:/FK/StocksInfo.xlsx')['ts_code'].tolist()
print(type(df_codes))