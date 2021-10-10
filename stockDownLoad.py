import tushare as ts


import pandas as pd 
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
def down_stocksinfo():
    data=pro.stock_basic()
    data.to_excel('C:/FK/StocksInfo.xlsx')  
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
pro = ts.pro_api('ebe4734e785004ada3e0f4e03da59a5dee8c7da0b7820ce5c50fb30e')
ip='127.0.0.1'
user='stock'
pwd='stock'
db='stockdb'



# engine = create_engine(f'mysql+pymysql://{user}:{pwd}@{ip}:3306/{db}')

# conn = pymysql.connect(host=ip,user=user,password=pwd,database=db,charset='utf8')
# cursor = conn.cursor()
# cursor.execute(sql)
#
# for code in get_allstocks()['ts_code']:
#     down_stdailys(code,st_date,ed_date)
    
 
# df_cal = pro.trade_cal(start_date=20210101,end_date=20210529,exchange='SSE')
# df_cal.to_excel('D:/tra_date.xlsx')  

#获取日期

###主函数
# for i in dates:
    #获取每天的涨跌数量

# print(df[df.ts_code.str.contains('^300')].pct_chg)
# df_up=df[df.ts_code.str.contains('^300')& df.pct_chg>0]
# df_down=df[df.ts_code.str.contains('^300')& df.pct_chg<0]

def down_stocks(path,start,end):
    st_date=start 
    ed_date=end 
    df_codes = pd.read_excel('%s/StocksInfo.xlsx' %path)['ts_code'].tolist()
    for i in df_codes:
        try:
            df= pro.daily(ts_code=i,start_date=st_date,end_date=ed_date)#遍历每天行情
            df.to_excel(f'%s/local_stock/{i}.xlsx' %path)
            # df_codes.remove(i)
            print('%s完成下载' %i)
        except:
            print('%s 失败' %i)
            df= pro.daily(ts_code=i,start_date=st_date,end_date=ed_date)#遍历每天行情
            df.to_excel(f'C:/FK/local_stock/{i}.xlsx')
            print('%s完成下载' %i)   
        continue         
path = 'C:/FK'
down_stocks(path,20100101,20211010)
# down_stocksinfo()