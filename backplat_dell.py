'''
1保证回测功能
2验证回测准确性
3完成封装
'''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from backtrader import broker  # For datetime objects
import tushare as ts
# Import the backtrader platformr
import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import matplotlib.pyplot as plt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
from tushare.pro.data_pro import FACT_LIST
import fk

    
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
    def log(self, txt, dt=None,doprint=False):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    
    def __init__(self):
        #这里用了虚拟下标d，作用同唯一标识，有些地方用tscode
        #indx赋值,bt指标使用datas[i]处理
        self.inds=dict()
        for i,d in enumerate(self.datas):
            print(self.)
            self.inds[d]=bt.ind.SMA(d.close,period=self.p.min_period)

            bt.indicators.ExponentialMovingAverage(self.datas[i], period=self.p.min_period)
            bt.indicators.WeightedMovingAverage(self.datas[i], period=self.p.min_period).subplot = True
            bt.indicators.StochasticSlow(self.datas[i])
            bt.indicators.MACDHisto(self.datas[i])
            rsi = bt.indicators.RSI(self.datas[i])
            bt.indicators.SmoothedMovingAverage(rsi, period=self.p.min_period)
            bt.indicators.ATR(self.datas[i]).plot = False
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.size=0
        # self.sma = bt.indicators.SimpleMovingAverage(
        #     self.datas[0], period=self.params.maperiod)
        # # 十日移动平均线
        # self.sma21 = bt.indicators.SimpleMovingAverage(
        #     self.datas[0], period=21)
 
        
        
        

    def notify_order(self, order):
        #订单状态处理
            if order.status in [order.Submitted, order.Accepted]:
                # Buy/Sell order submitted/accepted to/by broker - Nothing to do
                return
    
            # 买入卖出订单处理
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log('买入单价: %.2f, 买入总金额: %.2f, 手续费 %.2f,数量%.2f'%
                    (order.executed.price,
                     order.executed.value *-1,
                     order.executed.comm,
                     order.executed.size))

                elif order.issell():
                    self.log('卖出单价: %.2f, 总资产: %.2f, 手续费 %.2f,数量:%.2f' %
                    (order.executed.price,
                     self.broker.get_cash(),
                     order.executed.comm,
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
        #放在最前面，因为多股需要遍历操作
        #持仓赋值
        
        for i,d in enumerate(self.datas):
            
            vol = self.getposition(d)
            #触发条件：t-4日前高于21线，t-1低于21线，t突破21，t+1开盘价买入，5日后卖出

            if d.close[-4]>self.inds[d][-4] and d.close[-1]<self.inds[d][-1] and d.close[0]>self.inds[d][0]:
                self.order=self.buy(data=d,size=(0.1*self.broker.getvalue()//d.close))
            elif vol:
                if len(self)>=(self.bar_executed + self.params.exitbars):
                    self.order=self.sell(data=d,size=self.getposition(d).size)
                    



 
def runstart():
    cerebro = bt.Cerebro()
    
    #画图
    b = Bokeh(style='bar', plot_mode='single', scheme=Tradimo())
    

    #数据加工清洗:
    #for d in fk.get_cyb:
    
    #for code in stockpool:
    stockpool = fk.get_cyb().tolist()

    
    for code in stockpool:
        file = 'C:/FK/local_stock/%s.xlsx' %code
        df = pd.read_excel(file)
        if df.empty:
            break
        else:
            #数据-加工, format加上不然出现1970时间坑爹
            df['trade_date']=pd.to_datetime(df['trade_date'],format='%Y%m%d')
            df=df.rename(columns={'vol':'volume'})
            df.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
            df = df.sort_index(ascending=True)  #从小到大
            df['openinterest']=0
            df=df[['open','high','low','close','volume','openinterest']]
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data,name=code)

        

    
    cerebro.addstrategy(MyStrategy)
    #指标设置
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SP') #夏普
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='AR')#每年化收益率
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DD')#回撤
    cerebro.addanalyzer(bt.analyzers.Returns, _name='RE') #收益率
   
    
    
 
    
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
    cerebro.plot(b)
    # cerebro.plot(style='candle')
    print('最终收益: %.2f' % cerebro.broker.getvalue())
    
if __name__ == '__main__':
    stockpools=['600884.sh','601012.sh','300059.sz']
    pro = ts.pro_api('ebe4734e785004ada3e0f4e03da59a5dee8c7da0b7820ce5c50fb30e')
    runstart()
    
    
    
    
    
    
    
    