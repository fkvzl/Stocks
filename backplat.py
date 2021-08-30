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
import tushare as ts
# Import the backtrader platform
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd


class TestStrategy(bt.Strategy):
    '''
    近5日累计负数和<-5且作日收盘<21线，今日收盘>21线。买入
    T+5收盘卖出
    '''
    params = (
            ('maperiod', 15),
        )
    #日志格式
    def log(self, txt, dt=None,doprint=True):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    
    def __init__(self):
        #初始化变量
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        self.sma5 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=5)
        # 十日移动平均线
        self.sma21 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=21)
        
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
    
    def notify_order(self, order):
        #订单状态处理
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return
    
            # Check if an order has been completed
            # Attention: broker could reject order if not enough cash
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('BUY EXECUTED, price:%.2f,cost:%.2f,comm:%.2f' % 
                             (order.executed.price,order.executed.value,order.executed.comm ))
                    self.buycomm = order.executed.comm
                elif order.issell():
                    self.log('SELL EXECUTED,price:%.2f,cost:%.2f,comm:%.2f' % 
                             (order.executed.price,order.executed.value,order.executed.comm ))
                                     
                self.bar_executed = len(self)
    
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')
    
            # Write down: no pending order
            self.order = None
            
    def next(self):
      # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

 
def runstart():
    #数据-获取
    df = pro.daily(ts_code='000001.SZ',start_date=20210101)
    #数据-加工
    df['trade_date']=pd.to_datetime(df['trade_date'])
    df=df.rename(columns={'vol':'volume'})
    df.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
    df = df.sort_index(ascending=True)  #从小到大
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]

    #回测-数据范围
    data = bt.feeds.PandasData(dataname=df)
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    cerebro.adddata(data)
    
    #回测-资金规则
    cerebro.broker.setcash(100000.0)  #总资产
    cerebro.addsizer(bt.sizers.FixedSize,stake=1000)
    cerebro.broker.setcommission(0.0005)
    
    # cerebro.plot()
    #回测-启动
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
if __name__ == '__main__':
    pro = ts.pro_api('ebe4734e785004ada3e0f4e03da59a5dee8c7da0b7820ce5c50fb30e')
    runstart()
    
    
    
    
    
    
    
    