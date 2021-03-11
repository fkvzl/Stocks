import xcsc_tushare as ts
import pandas
import datetime
import pymysql

#db链接
# =============================================================================
# def db_conn(col,table):
#     #连客户端
#     
# =============================================================================
    

 
    
#token、开发环境的使用
ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
pro = ts.pro_api(env='prd')
 

# 日期遍历 begin——end
# =============================================================================
# begin=datetime.date(2021,3,1)
# end=datetime.date(2021,3,2)
# for i in range((end-begin).days+1):
#     day=begin+datetime.timedelta(days=i)
#     delta=day.strftime('%Y%m%d')
#     
#     #获取当天delta行情，存入数据库daily表
#     df = pro.daily(trade_date=delta)
#     db_conn(df,"daily")
# =============================================================================
    

conn = pymysql.connect(host="127.0.0.1",user="stock",password="stock",database="stockdb",charset="utf8")
cursor = conn.cursor()
cursor.execute("SELECT * from test")
data = cursor.fetchone()
print (data)
conn.close()