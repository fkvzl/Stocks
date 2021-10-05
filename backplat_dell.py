'''
1保证回测功能
2验证回测准确性
3完成封装
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
from backtrader import broker  # For datetime objects
import tushare as ts
# Import the backtrader platformr
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import matplotlib.pyplot as plt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
import fk


class MyStrategy(bt.Strategy):
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
        print("----------------start---------------")
        print(self.datas[0].datetime.date[0])
        print(self.datas[0].datetime.date[-1])
        print(self.datas[-1].datetime.date[0])
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        # 十日移动平均线
        self.sma21 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=21)
 
        
        #费用
        self.buyprice = None
        self.buycomm = None
        self.size=0
        
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
                    self.log('买入单价: %.2f, 总金额: %.2f, 手续费 %.2f,数量%d'%
                    (order.executed.price,
                     order.executed.value *-1,
                     self.broker.get_cash(),
                     #order.executed.comm,
                     self.getposition().size))

                elif order.issell():
                    print(order.executed.size)

                    self.log('卖出单价: %.2f, 总金额: %.2f, 手续费 %.2f,数量:%s' %
                    (order.executed.price,
                     self.broker.get_cash(),
                     #order.executed.comm,
                     self.broker.get_cash(),
                     order.executed.size))
                                     
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
            
            self.order=self.buy(size=0.1*self.broker.getvalue())
                
        # print('today:%s,%s'%(self.datas[0].datetime.date(0),self.order))
        #卖出必须在买入有头寸之后
        elif self.position:
            if len(self)>=(self.bar_executed + self.params.exitbars):
                self.order=self.sell()
                    



 
def runstart():
    cerebro = bt.Cerebro()
    
    #画图
    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    

    #数据加工清洗:
    #for d in fk.get_cyb:
    stockpool=['600884.sh','601012.sh']
    for code in stockpool:
        codename=code
        df = pro.daily(ts_code=code,start_date=20210101)
     #数据-加工
        df['trade_date']=pd.to_datetime(df['trade_date'])
        df=df.rename(columns={'vol':'volume'})
        df.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
        df = df.sort_index(ascending=True)  #从小到大
        df['openinterest']=0
        df=df[['open','high','low','close','volume','openinterest']]
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data,name=code)


    
    cerebro.addstrategy(MyStrategy)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SR')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    
    
 
    
    #回测-资金规则(总资产和手续费)
    cerebro.broker.setcash(100000.0) 
    cerebro.broker.setcommission(0.0003)
    
    # cerebro.plot()
    #回测-启动
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    results = cerebro.run()
    result = results[0]

    cerebro.plot(b)
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('SR:',result.analyzers.SR.get_analysis())
    print('DW:',result.analyzers.DW.get_analysis())
    
if __name__ == '__main__':
    pro = ts.pro_api('ebe4734e785004ada3e0f4e03da59a5dee8c7da0b7820ce5c50fb30e')
    runstart()
    
    
    
    
    
    
    
    