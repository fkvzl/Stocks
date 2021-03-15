【环境搭建】
--1管理员启动数据库，
>net start mysql
>mysql -u stock -p    进入 ，密码回车

--2安装python3的mysql用 
 >pip install pymysql

--3创建股票字段表stdaily,change反引号表示特殊

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