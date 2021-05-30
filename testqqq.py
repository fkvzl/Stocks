# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
df_date = pd.read_excel('D:/tra_date.xlsx')
 
plt.figure()
plt.subplots(figsize=(30,10))
#fig, axs = plt.subplots(figsize=(100, 100))
plt.plot(df_date.trade_date,df_date.up)

plt.show()
##主函数