#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# coding=utf-8

import pandas as pd
import get_date as gd
import tushare as ts
from sqlalchemy import create_engine

from mysql_tables_structure import Base
import mysql_functions as mf
import pymysql

import tushare_data as td

# 创建数据库引擎
engine = create_engine("mysql://root:mysql@localhost/stockvision?charset=utf8")
conn = engine.connect()

db=pymysql.connect(host="localhost", user="root", passwd="mysql", db="stockvision")
# 创建mysql所有表结构
Base.metadata.create_all(engine)

# 连接 tushare
ts.set_token("5e2ad725eacd63551be36913a89266136d834a92776c7a9c9a41b468")
pro = ts.pro_api()

# 股票列表
# mf.update_stock_basic(engine, pro, 3, 2)

# mf.upadte_index_basic(engine,pro,3,2)

# 根据需要增删 日线行情 数据  单次提取*4000*条
# mf.delete_daily(engine, '19901219', '20191231')

start_date = '20171201'
end_date = '20180301'

date_list = gd.get_date_list(start_date, end_date)

df=pd.read_sql("select ts_code from index_basic where market='SSE'",db)
indexs=list(df['ts_code'])
mf.update_index_weight_by_index(engine,pro,indexs,start_date,end_date,3,2)

# indexes=["000001.SH","399001.SZ","000016.SH","000905.SH","399005.SZ"]

# mf.update_index_weight_by_index(engine, pro, indexes, 3, 2)

# 个股每日指标
# mf.update_daily_basic_date(engine, pro, start_date, end_date, 3, 2)

# 大盘日线行情
# mf.update_index_daily_date(engine, pro, start_date, end_date, 3, 2)
# 大盘每日指标
# mf.update_index_daily_basic_date(engine, pro, start_date, end_date, 3, 2)
#
# mf.update_trade_cal(engine, pro, 'SSE', start_date, end_date, 3, 2)
# mf.update_trade_cal(engine, pro, 'SZSE', start_date, end_date, 3, 2)
"""
# 股票代码方式更新 日线行情
codes = mf.get_ts_code(engine)
mf.update_all_daily(engine, pro, codes, '19901219', '20051231', 3, 2)


# 注意：不能添加表中已有的日期
start_date = '20130320'
#end_date = '20130319'
end_date = '20171231'
date_list = gd.get_date_list(start_date, end_date)
for day in date_list:
    print(day)
    mf.update_daily_date(engine, pro, day, 3, 2)
"""
