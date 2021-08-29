
pip install tushare
pip install backtrader
pip uninstall matplotlib
pip install matplotlib==3.2.2

pip install backtrader_plotting
【环境搭建】
--1管理员启动数据库，
>net start mysql
>mysql -u stock -p    进入 ，密码回车

--2安装python3的mysql用 
 >pip install pymysql

--3创建股票字段表stdaily,change反引号表示特殊
GRANT ALL ON *.* TO 'stock'@'%';

create database stdaily;

CREATE TABLE IF NOT EXISTS stdaily(
   ts_code VARCHAR(40) NOT NULL,
   trade_date VARCHAR(40) NOT NULL,
   crncy_code VARCHAR(40),
   pre_close INT,
   open INT,
   high INT,
   low INT,
   close INT,
   `change` INT ,
   pct_chg INT,
   volume INT,
   amount INT,
   adj_pre_close INT,
   adj_open INT,
   adj_high INT,
   adj_low INT,
   adj_close INT,
   adj_factor INT,
   avg_price INT,
   trade_status VARCHAR(40),
   PRIMARY KEY ( ts_code,trade_date )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

--导入

20210315-完成全股票2021.1月份取数；完成全股票2010.1-2020.12.31取数

--安装ta-lib，官网只有32位，https://www.lfd.uci.edu/~gohlke/pythonlibs/ 网页上下载64位
1下载
2执行pip install TA_Lib-0.4.19-cp38-cp38-win_amd64.whl    --python版本是38要对应cp版本



【回测平台搭建】
1账户类
---策略
买入触发器
卖出触发器
---策略
2回测函数backtest
3选股模型集合




