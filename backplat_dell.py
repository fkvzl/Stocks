'''
1保证回测功能
2验证回测准确性
3完成封装
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from backtrader import broker
from backtrader.order import Order  # For datetime objects
from backtrader import num2date
import tushare as ts
# Import the backtrader platformr
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd

import os
import pyfolio as pf
    
class MyStrategy(bt.Strategy):
    '''
    近5日累计负数和<-5且作日收盘<21线，今日收盘>21线。买入
    T+5收盘卖出
    '''
    
    params = dict(
        exitbars = 5,
        min_period = 21,
    )
    #日志格式
    def log(self, txt, dt=None,doprint=True):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    
    def __init__(self):

        #这里用了虚拟下标d，作用同唯一标识，有些地方用tscode
        #indx赋值,bt指标使用datas[i]处理
        self.inds=dict()
        self.holDay=dict()

        for i,d in enumerate(self.datas):
            self.inds[d]=bt.indicators.SMA(d.close,period=self.p.min_period)
        #    bt.indicators.ExponentialMovingAverage(self.datas[i], period=self.p.min_period)
        #    bt.indicators.WeightedMovingAverage(self.datas[i], period=self.p.min_period).subplot = True
        #    bt.indicators.StochasticSlow(self.datas[i])
        #    bt.indicators.MACDHisto(self.datas[i])
        #    rsi = bt.indicators.RSI(self.datas[i])
        #    bt.indicators.SmoothedMovingAverage(rsi, period=self.p.min_period)
        #    bt.indicators.ATR(self.datas[i]).plot = False
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.size=0
        # self.sma = bt.indicators.SimpleMovingAverage(
        #     self.datas[0], period=self.params.maperiod)
        # # 十日移动平均线
        # self.sma21 = bt.indicators.SimpleMovingAverage(
        #     self.datas[0], period=21)
 
    def next(self):
        '''
        1前提判断
        2买入
        3卖出
        '''
        #放在最前面，因为多股需要遍历操作
        #持仓赋值
        
        for d in self.datas[1:]:
            #获取今日，昨日，前日，大前日价格
            p0_close = d.close[0]
            p1_close = d.close[-1]
            p2_close = d.close[-2]
            p3_close = d.close[-3]

            #如果出现涨停，涨停，阴线，打印股票及日期
            if ((p2_close> p3_close*1.1-0.02) and
                (p1_close>p2_close*1.1-0.02) and
                (p0_close<p1_close*.97)):
                    self.log(f"{d.datetime.date(0)},{d._name}")

        
        

    def notify_order(self, order):
        #订单状态处理
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return
    
            # 买入卖出订单处理
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('买入%s, 单价: %.2f, 总资产: %.2f, 手续费 %.2f,数量%.2f'%
                    ( 
                    order.p.data._name,
                     order.executed.price,
                     self.broker.get_value(),
                     order.executed.comm,
                     order.executed.size))

                elif order.issell():
                    self.log('卖出%s, 单价: %.2f, 总资产: %.2f, 手续费 %.2f,数量:%.2f' %
                    (order.p.data._name,order.executed.price,
                     self.broker.get_value(),
                     order.executed.comm,
                     order.executed.size))
                                     
                self.bar_executed = len(self)
    
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('订单取消/保证金不足/拒绝')
    
            # Write down: no pending order
            self.order = None
            

                    



 
############################################以上为策略部分#######################
cerebro = bt.Cerebro()
    
#画图
# b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
fileRoot = 'C:/FK/local_stock/'
fileList = sorted(os.listdir(fileRoot))
pro = ts.pro_api('ebe4734e785004ada3e0f4e03da59a5dee8c7da0b7820ce5c50fb30e')
    
for file in fileList:
    df = pd.read_excel(fileRoot+file)
    if len(df)<365:
        continue  #break是跳出整个for
    
    #数据-加工, format加上不然出现1970时间坑爹
    df['trade_date']=pd.to_datetime(df['trade_date'],format='%Y%m%d')
    df=df.rename(columns={'vol':'volume'})
    df.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
    df = df.sort_index(ascending=True)  #从小到大
    df['openinterest']=0
    df=df[['open','high','low','close','volume','openinterest']]
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data,name=file)

        

    
cerebro.addstrategy(MyStrategy)
#指标设置
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SP') #夏普
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AR')#每年化收益率
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DD')#回撤
cerebro.addanalyzer(bt.analyzers.Returns, _name='RE') #收益率
cerebro.addanalyzer(bt.analyzers.PyFolio) #资金曲线分析
    
    
    
    
#回测-资金规则(总资产和手续费)
cerebro.broker.setcash(100000.0) 
cerebro.broker.setcommission(0.0003)
    
    
#回测-启动
print('初始金额: %.2f' % cerebro.broker.getvalue())
back = cerebro.run()


#总份额，年化，回撤，夏普
ratio_list=[[
    x.analyzers.SP.get_analysis()['sharperatio'],#夏普比率
    x.analyzers.RE.get_analysis()['rtot']*100, #总复合收益率        
    x.analyzers.DD.get_analysis()['max']['drawdown'], #最大回撤
    x.analyzers.DD.get_analysis()['max']['len']]#最大回撤周期
    for x in back]  #夏普
ratio_df = pd.DataFrame(ratio_list,columns=['夏普','年化%','最大回撤','最大回撤周期'])
print(ratio_df)
print('历年收益率：%s' %back[0].analyzers.AR.get_analysis())#每年年化收益率
print('标准收益率：%s' %back[0].analyzers.RE.get_analysis()['rnorm100']) # 年化标准化回报以100%展示
print('最终总市值: %.2f' % cerebro.broker.getvalue())


#资金曲线
pyfoliozer = back[0].analyzers.getbyname('pyfolio')
returns,positions,transactions,gross_lev = pyfoliozer.get_pf_items()
pf.create_full_tear_sheet(
    returns,
    positions = positions,
    transactions = transactions,
)
    
    
    
    
    