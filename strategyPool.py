# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 10:23:10 2021
选股
@author: Administrator
"""
import tushare as ts
import pandas  as pd
import xlrd
import tblib  as tl
# pro = ts.pro_api(env='prd')

pro = ts.pro_api('a5cec5a238e77dabe416e44b53bb9fd679aa3c00a148cd47e315ef8e')





'''
1、talib的macd存在前33个null，自用macd已优化
2、使用时，整体周期取股票从发行以来（涉及递归，不支持取中间某段）
'''
def myMACD(price, fastperiod, slowperiod, signalperiod):
    ewma12 = price.ewm(span=fastperiod,adjust=False).mean()
    ewma60 = price.ewm(span=slowperiod,adjust=False).mean()
    dif = ewma12-ewma60
    dea =  dif.ewm(span=signalperiod,adjust=False).mean()
    bar = (dif-dea)*2 #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar


def myKDJ(low,high,close):
    low_list = low.rolling(9, min_periods=9).min()
    low_list.fillna(value = low.expanding().min(), inplace = True)
    high_list = high.rolling(9, min_periods=9).max()
    high_list.fillna(value = high.expanding().max(), inplace = True)
    rsv = (close - low_list) / (high_list - low_list) * 100

    df['K'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['D'] = df['K'].ewm(com=2).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    kdj_position=df['K']>df['D']   #k->d-0+金叉；k->d->0-死叉
    
    df.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_金叉死叉'] = '金叉'
    df.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_金叉死叉'] = '死叉'
    print(df)
    


'''
日线kdj
    1金叉：
    2死叉：
60分时kdj
    3金叉：
    4死叉：
'''
def kdj():
    global df
    df=pro.daily(ts_code='300905.SZ')
    df=df[::-1]
    myKDJ(df['low'],df['high'],df['close'])
    

 


 

'''
获取创业板股票
用法 for i in getstocks()


'''
def getStocks():
    stocks = pro.stock_basic()
    cyb_stock = stocks[stocks['ts_code'].str.contains('^30')]
    df_tscode = cyb_stock['ts_code'].values
    return (df_tscode)
    
    
'''
1、vr有多次冲高,底部抬高——》意图明显
def vr():
'''

    
'''
近T日股价是>-2
'''
# def overSZ(days):
        
    
    
    
'''
1创业板300+零轴up+零轴down+下限
2满足macd多
390天最低kdj

问题：
1macd值跨度大，无参考性
'''
def macdhist_300(days):
    for i in getStocks(): #获取全量股票
        try:
            df = pd.read_excel('C:/FK/local_stock/{i}.xlsx')
            df=df[::-1]  #倒序，同sort区别为sort为排序方式
            dif,dea,hist=myMACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
            hist = hist.values[days:]   #days要负数
            if  (len(hist [ (hist >=-0.1) * (hist <= 0.07)]))>=22:
                print(i)
        except:
            print('不可用：',i)

#全板块            
def macdhist_v1():
    df = pd.read_excel('C:/FK/ts_codes.xlsx')
    codes = df.ts_code.to_list()
    for i in codes:
        df = pd.read_excel('C:/FK/local_stock/%s.xlsx' %i)       
        df=df[::-1]  #倒序，同sort区别为sort为排序方式
        dif,dea,hist=myMACD(df['close'],fastperiod=12, slowperiod=26, signalperiod=9)
        hist = hist.values[-40:]   #days要负数
        if  (len(hist [ (hist >=-0.04) * (hist <= 0.04)]))>=22:
                print(i)
        
real = tl.TRIX(close, timeperiod=30)
         
            
            
            
            
            
'''
macd死叉后10天内又金叉（dif穿dea）
obv持续向上
boll没上方压力性


df_codes = pd.read_excel('C:/FK/StocksInfo.xlsx')
#ts_codes = [x for i,x in enumerate(ts_codes_all) if x.find('688')] #find找到返回0，其他-1，if的-1是true
ts_codes = df_codes[df_codes['ts_code'].str.contains('^300')].ts_code.values.tolist()
t = []
for i in ts_codes:
    print(i)
    ###数据源处理
    df = pd.read_excel(f'C:/FK/local_stock/{i}.xlsx')
    # 倒序，同sort区别为sort为排序方式,计算macd要上市日开始算起
    df = df[::-1]
    dif, dea, hist = myMACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    #获取近16一天的kd数据
    df['K'] = dif[-7:]
    df['D'] = dea[-7:]
    kds=df['K']>df['D']
    #shift表昨日 不能用未来数据。 false->true 金叉1  true->false死叉0
    df_c = df.copy()
    df_c['KDJ']='3'

    # print(df)
    df_c.loc[kds[(kds == True) & (kds.shift() == False)].index, 'KDJ'] = '1'
    df_c.loc[kds[(kds == False) & (kds.shift() == True)].index, 'KDJ'] = '0'
    df_c = df_c[-20:]
    # a = df['KDJ'].value_counts()["0"],该方法存在坐标越界bug
    # print(df_c)
    a = list(df_c['KDJ']).count("0")  #死叉个数
    b = list(df_c['KDJ']).count("1")  #金叉个数,因为首次必金叉所以》1
    # print(a)
    # print(b)
    #近10天开盘不能跌破20均线
    ###筛选出现一次死叉金叉股票
    if(a==1 and b==2 ):
        t.append(i)

print(t)
'''