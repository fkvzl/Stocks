import tushare as ts
import pandas as pd

# 下载所有股票基本信息
def down_stocksinfo():
    data = pro.stock_basic()
    data.to_excel('C:/FK/StocksInfo.xlsx')
    return data




# token、开发环境的使用
pro = ts.pro_api('a5cec5a238e77dabe416e44b53bb9fd679aa3c00a148cd47e315ef8e')



###主函数
# for i in dates:
# 获取每天的涨跌数量

# print(df[df.ts_code.str.contains('^300')].pct_chg)
# df_up=df[df.ts_code.str.contains('^300')& df.pct_chg>0]
# df_down=df[df.ts_code.str.contains('^300')& df.pct_chg<0]

def down_stocks():
    path = 'C:/FK'
    # st_date = start
    # ed_date = end

    #剔除688创业板
    df_codes_all = pd.read_excel('%s/StocksInfo.xlsx' % path)['ts_code'].tolist()
    df_codes = [x for i,x in enumerate(df_codes_all) if x.find('688')]

    #循环行情
    for i in df_codes:
        try:
            df = pro.daily(ts_code=i)  # 遍历每天行情
            # df = pro.daily(ts_code=i, start_date=st_date, end_date=ed_date)  # 遍历每天行情
            df.to_excel(f'%s/local_stock/{i}.xlsx' % path)
            print('%s完成下载' % i)
        except:
            print('%s 失败' % i)
            # df = pro.daily(ts_code=i, start_date=st_date, end_date=ed_date)  # 遍历每天行情
            df = pro.daily(ts_code=i)  # 遍历每天行情
            df.to_excel(f'C:/FK/tmp/{i}.xlsx')
            print('%s完成下载' % i)
        continue
    print('download success!!!')

# 涨涨跌票筛选
def get_zt():
    path = 'C:/FK/local_stock'
    df_codes = pd.read_excel('%s/StocksInfo.xlsx' % path)['ts_code'].tolist()
    zt = []

    # 获取涨停日>2
    for i in df_codes:
        df = pd.read_excel(f'%s/{i}.xlsx' % path)

        # 剔除科创
        df = df[~ df['ts_code'].str.contains('^688')]
        if (df[df['pct_chg'] > 9.7].ts_code.count()) == 2:
            zt.append(i)
    # 二次筛选当天是跌的
    zt_copy = zt.copy()
    for i in zt_copy:
        df = pro.daily(ts_code=i, trade_date=20211230)
        if (df['pct_chg'].values) > 0:
            zt.remove(i)


down_stocks()