--1管理员启动数据库，
>net start mysql
>mysql -u stock -p    进入 ，密码回车

--2安装python3的mysql用 
 >pip install pymysql

--3创建股票字段表stock_base


CREATE TABLE IF NOT EXISTS `runoob_tbl`(
   `runoob_id` INT UNSIGNED AUTO_INCREMENT,
   `runoob_title` VARCHAR(100) NOT NULL,
   `runoob_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `runoob_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;