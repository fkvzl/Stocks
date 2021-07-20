'''
1保证回测功能
2验证回测准确性
3完成封装
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import xcsc_tushare as ts
# Import the backtrader platform
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd




def getData(file):
    df = pd.read_excel(file) 
    return df
def runstart():
    #数据-获取
    df = getData(file)
    
    #数据-加工
    df['trade_date']=pd.to_datetime(df['trade_date'])
    df.rename(columns={'vol':'volume'})
    df.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
    df = df.sort_index(ascending=True) 
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]

    #回测-准备
    data = bt.feeds.PandasData(dataname=df)
    cerebro = bt.Cerebro()
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    
    
    #回测-启动
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    
if __name__ == '__main__':
    file = 'F:/stockfiles/000001.SZ.xlsx'
    runstart()
    
    
    
    
    
    
    
    