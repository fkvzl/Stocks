'''
1保证回测功能
2验证回测准确性
3完成封装
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import tushare as ts
# Import the backtrader platformr
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import matplotlib.pyplot as plt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo



class TestStrategy(bt.Strategy):
    '''
    近5日累计负数和<-5且作日收盘<21线，今日收盘>21线。买入
    T+5收盘卖出
    '''
    
    params = (
        ('exitbars',5),
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
        
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        # 十日移动平均线
        self.sma21 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=21)
        #近5日价格，近5日负数价格
        
        #费用
        self.buyprice = None
        self.buycomm = None
        
        
        #绘图
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0]).plot = False
        
    def notify_order(self, order):
        #订单状态处理
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return
    
            # 买入卖出订单处理
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('买入单价: %.2f, 金额: %.2f, 手续费 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                elif order.issell():
                    self.log('卖出单价: %.2f, 金额: %.2f, 手续费 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                                     
                self.bar_executed = len(self)
    
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('订单取消/保证金不足/拒绝')
    
            # Write down: no pending order
            self.order = None
            
    def next(self):
        '''
        1前提判断
        2买入
        3卖出
        '''
        #如果正在下单，不提交二次订单
        if self.order:
            return
        
        #只要触发就买
        #触发条件：t-4日前高于21线，t-1低于21线，t突破21，t+1开盘价买入，5日后卖出
        if self.dataclose[-4]>self.sma21[-4] and self.dataclose[-1]<self.sma21[-1] and self.dataclose[0]>self.sma21[0]:
            self.order=self.buy()
                
        # print('today:%s,%s'%(self.datas[0].datetime.date(0),self.order))
        #卖出必须在买入有头寸之后
        elif self.position:
            if len(self)>=(self.bar_executed + self.params.exitbars):
                self.order=self.sell()
                    



 
def runstart():
    #数据-获取
    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())

    df = pro.daily(ts_code='600328.SZ',start_date=20210301)
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
    codename='300005'
    cerebro.adddata(data,name=codename)
    
    #回测-资金规则(总资产和手续费)
    cerebro.broker.setcash(100000.0) 
    cerebro.addsizer(bt.sizers.FixedSize,stake=10)
    cerebro.broker.setcommission(0.0005)
    
    # cerebro.plot()
    #回测-启动
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    cerebro.plot(b)
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
if __name__ == '__main__':
    pro = ts.pro_api('ebe4734e785004ada3e0f4e03da59a5dee8c7da0b7820ce5c50fb30e')
    runstart()
    
    
    
    
    
    
    
    