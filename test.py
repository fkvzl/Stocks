# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 22:09:25 2021

@author: fkvzl
"""
import pandas as pd
stockpool=['600884.sh','601012.sh','300059.sz']
for s in stockpool:
    file = 'C:/FK/local_stock/%s.xlsx' %s
    df = pd.read_excel(file)
    print (df)