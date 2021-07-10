from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import xcsc_tushare as ts
# Import the backtrader platform
import backtrader as bt
import pandas as pd






if __name__ == '__main__':
    
    ts.set_token('db359948bb4351fe9731151b3ad7925b240419250d16094af141acd5')
    pro = ts.pro_api(env='prd')
    df = pro.daily(ts_code='000001.SZ', start_date='20210625', end_date='20210628')
    df['trade_date']=pd.to_datetime(df['trade_date'])
    df = df.rename(columns={'vol','volume'})
    df.set_index=('trade_date')
    df = df.sort_index(ascending=True)
    df['openinterest']=0
    
    
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    data = bt.feeds.YahooFinanceCSVData(
        dataname=df,
        # Do not pass values before this date
        fromdate=datetime.datetime(2021, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2021, 6, 28)
        )
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())