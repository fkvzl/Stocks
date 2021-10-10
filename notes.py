# -*- coding: utf-8 -*-
"""
Created on Fri May 14 08:20:13 2021

@author: fkvzl

E-mail:fkvzl@qq.com

主题：python笔记
思路：

"""
【学习路线】
1【ok】回测案例实现
2【ing】第一个回测策略实现

【基础语法】
1、dataframe.count()：用来统计每行/每列的数量，精确级别
2、取列，用df.列名1，或者df['列名1'] ;拓展：df['K']表示新增一列K字段
3、取行，用loc
3、上交所6开头SH，其他SZ

【技术指标】
macd跟kdj要自己写，talib中默认前33数值为NA

[金工]
华泰金工

20211007
重新拉代码用如下 git checkout -- backplat_dell.py 
解决self.buy存在数量非整数，用//向下取余对self.buy的size定义解决，打印的时候注意%d跟%s区别，d会截取整数