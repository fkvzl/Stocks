import xcsc_tushare as ts
import pandas as pd 
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
    data.to_excel('D:/StocksInfo.xlsx')  
    return data


#获取股票信息
def get_allstocks():
    data = pd.read_excel('D:/StocksInfo.xlsx')
    return data

def down_stdailys(code,start,end):  #遍历每个股票代码
    df = pro.daily(ts_code=code,start_date=start,end_date=end)#遍历每天行情
    data = pd.read_sql_query(f"select * from stdaily where ts_code='{code}'",con=engine)

    
    
    if df.empty or  not data.empty:
        print(f'股票:{code}无需登记')
    else:
        try:
            df.to_sql('stdaily', engine,index=False,if_exists='append')
            
        except:
            pass
        else:
            df.to_excel(f'F:/stock/{code}.xlsx')
            print(f'股票:{code}下载完成')
    
    
#######################################以上为函数调用###################################



#token、开发环境的使用
ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')

ip='127.0.0.1'
user='stock'
pwd='stock'
db='stockdb'

st_date=20210101
ed_date=20210529

# engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{ip}:3306/{db}')

# conn = pymysql.connect(host=ip,user=user,password=pwd,database=db,charset='utf8')
# cursor = conn.cursor()
# cursor.execute(sql)
#
# for code in get_allstocks()['ts_code']:
#     down_stdailys(code,st_date,ed_date)
    
 
# df_cal = pro.trade_cal(start_date=20210101,end_date=20210529,exchange='SSE')
# df_cal.to_excel('D:/tra_date.xlsx')  
df_date = pd.read_excel('D:/tra_date.xlsx')
#获取日期
dates = df_date.trade_date.values

###主函数
# for i in dates:
    #获取每天的涨跌数量
df=pro.daily(trade_date=20210104)
# print(df[df.ts_code.str.contains('^300')].pct_chg)
# df_up=df[df.ts_code.str.contains('^300')& df.pct_chg>0]
# df_down=df[df.ts_code.str.contains('^300')& df.pct_chg<0]

# print(df_down)
 
