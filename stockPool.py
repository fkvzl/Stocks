# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:23:10 2021

@author: Administrator
"""

import talib as tl
MACD_macd= tl.MACD(5.37, fastperiod=12, slowperiod=21, signalperiod=9)
print(MACD_macd)
