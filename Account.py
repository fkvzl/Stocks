# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:18:17 2021

@author: Administrator
"""


class Account:

    def __init__(self, money_init, start_date='', end_date=''):
        self.cash = money_init  # 现金
        self.stock_value = 0  # 股票价值
        self.market_value = money_init  # 总市值
        self.stock_name = []  # 记录持仓股票名字
        self.stock_id = []  # 记录持仓股票id
        self.buy_date = []  # 记录持仓股票买入日期
        self.stock_num = []  # 记录持股股票剩余持股数量
        self.stock_price = []  # 记录股票的买入价格
        self.start_date = start_date
        self.end_date = end_date
        self.stock_asset = []  # 持仓数量
        self.buy_rate = 0.0003  # 买入费率
        self.buy_min = 5  # 最小买入费率
        self.sell_rate = 0.0003  # 卖出费率
        self.sell_min = 5  # 最大买入费率
        self.stamp_duty = 0.001  # 印花税
        self.info = []  # 记录所有买入卖出记录
        self.max_hold_period = 5  # 最大持股周期
        self.hold_day = []  # 股票持股时间

        self.cost = []  # 记录真实花费
        # self.profit = []  # 记录每次卖出股票收益

        self.stop_loss_rate = -0.03  # 止损比例
        self.stop_profit_rate = 0.05  # 止盈比例

        self.victory = 0  # 记录交易胜利次数
        self.defeat = 0  # 记录失败次数

        self.cash_all = [money_init]  # 记录每天收盘后所持现金
        self.stock_value_all = [0.0]  # 记录每天收盘后所持股票的市值
        self.market_value_all = [money_init]  # 记录每天收盘后的总市值
        self.max_market_value = money_init  # 记录最大的市值情况，用来计算回撤
        self.min_after_max_makret_value = money_init  # 记录最大市值后的最小市值
        self.max_retracement = 0  #记录最大回撤概率
