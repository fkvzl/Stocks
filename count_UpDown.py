import xcsc_tushare as ts
import pandas as pd 
import datetime
import pymysql
from sqlalchemy import create_engine

 
    

 



    
def db_conn(ip,user,pwd,db,sql):
    conn = pymysql.connect(host=ip,user=user,password=pwd,database=db,charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    print (data)
    conn.close()
# df=pro.daily(trade_date=20210310)



#db_conn(ip,user,pwd,db,sql)



# trade_ds=pro.trade_cal(exchange='SSE', start_date=st_date, end_date=ed_date,fields='trade_date')
# for d in trade_ds['trade_date'].values:   #遍历交易日期d
#     print(pro.daily(trade_date=d,fields='ts_code,trade_date,pre_close,open,high,low,close,pct_chg,amount'))

#下载所有股票基本信息
def down_stocks():
    data=pro.stock_basic()
    data.to_excel('D:/stock/StocksInfo.xlsx')  
    return data


#获取股票信息
def get_allstocks():
    data = pd.read_excel('D:/stock/StocksInfo.xlsx')
    return data

def down_stockdata(ts_code,start,end):  #遍历每个股票代码
    df = pro.daily(ts_code=code,start_date=start,end_date=end)#遍历每天行情
    df.to_sql('stdaily', engine,index=False,if_exists='replace')
        
    if df.empty:
        print(f'股票:{ts_code}无记录')
    else:
        df.to_excel(f'D:/stock/{ts_code}.xlsx')
        print(f'股票:{ts_code}下载完成')
    
    
#######################################以上为函数调用###################################



#token、开发环境的使用
ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')

ip='127.0.0.1'
user='stock'
pwd='stock'
db='stockdb'

st_date=20210301
ed_date=20210302

engine=create_engine(f'mysql+pymysql://{user}:{pwd}@{ip}:3306/{db}')

# conn = pymysql.connect(host=ip,user=user,password=pwd,database=db,charset='utf8')
# cursor = conn.cursor()
# cursor.execute(sql)

# for code in get_allstocks()['ts_code']:
#     down_stockdata(code,st_date,ed_date)
#     ''
        
 
df = pro.daily(ts_code='600023.SH' ,start_date=st_date,end_date=ed_date)


        
