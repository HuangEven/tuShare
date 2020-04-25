#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# coding=utf-8
import time

import pandas as pd
import tushare_data as td
import get_date as gdte


def truncate_update(engine, data, table_name):
    """删除mysql表所有数据，to_sql追加新数据"""
    conn = engine.connect()
    conn.execute('truncate ' + table_name)
    data.to_sql(table_name, engine, if_exists='append', index=False)


def upadte_index_basic(engine, pro, retry_count, pause):
    """更新 指数信息 """
    markets = ['MSCI', 'CSI', 'SSE', 'SZSE', 'CICC', 'SW', 'OTH']
    data = pd.DataFrame()
    for market in markets:
        frame = td.get_index_basic(pro, market, retry_count, pause)
        print(frame.head())
        print(frame.columns)
        data = data.append(frame)

    data.to_sql('index_basic', engine, if_exists='append', index=False)


def get_ts_code(engine):
    """查询ts_code"""
    return pd.read_sql('select ts_code from stock_basic', engine)


def delete_daily(engine, start_date, end_date):
    """删除 日线行情 数据"""
    conn = engine.connect()
    conn.execute('delete from daily where  trade_date between ' + start_date + ' and ' + end_date)


def update_all_daily(engine, pro, codes, start_date, end_date, retry_count, pause):
    """股票代码方式更新 日线行情"""
    for value in codes['ts_code']:
        df = td.get_daily_code(pro, value, start_date, end_date, retry_count, pause)
        df.to_sql('daily', engine, if_exists='append', index=False)
        time.sleep(0.6)


def update_daily_date(engine, pro, date, retry_count, pause):
    """日期方式更新 日线行情"""
    df = td.get_daily_date(pro, date, retry_count, pause)
    df.to_sql('daily', engine, if_exists='append', index=False)


# 经测试一次最多只能调取4000行数据；
# 以一年数据测试，请求次数似乎没有限制【也可能是因为测试时只有一个线程，单位时间（比如1分钟）内请求次数较少】
def update_daily_basic_date(engine, pro, startDate, endDate, retry_count, pause):
    """日期方式更新 每日指标"""
    dates = gdte.get_date_list(startDate, endDate)
    df = pd.DataFrame()
    for date in dates:
        frame = td.get_daily_basic_date(pro, date, retry_count, pause)
        df = df.append(frame)
    df.fillna(value=0, inplace=True)
    # print(df.columns[df.isnull().any()].tolist())
    df.to_sql('daily_basic', engine, if_exists='append', index=False)


def update_index_daily_basic_date(engine, pro, startDate, endDate, retry_count, pause):
    """日期方式更新 大盘每日指标"""
    df = td.get_index_daily_basic_date(pro, startDate, endDate, retry_count, pause)
    # df = clean_df_db_dups(df, 'index_daily_basic', engine, dup_cols=['ts_code', 'trade_date'])
    df.to_sql('index_daily_basic', engine, if_exists='append', index=False)


# tushare注明单次调取最多8000行,测试结果看各属性值都能获取
def update_index_daily_date(engine, pro, startDate, endDate, retry_count, pause):
    """日期方式更新 大盘日线行情"""
    # 大盘指数ts_code
    codes = ['000001.SH', '000300.SH', '000905.SH', '399001.SZ', '399005.SZ', '399006.SZ', '399016.SZ', '399300.SZ ']
    df = pd.DataFrame()
    for code in codes:
        frame = td.get_index_daily_date(pro, code, startDate, endDate, retry_count, pause)
        df = df.append(frame)
        # df = clean_df_db_dups(df, 'index_daily', engine, dup_cols=['ts_code', 'trade_date'])
    df.to_sql('index_daily', engine, if_exists='append', index=False)


def update_stock_basic(engine, pro, retry_count, pause):
    """更新 股票信息 所有数据"""
    data = td.get_stock_basic(pro, retry_count, pause)
    data.to_sql('stock_basic', engine, if_exists='append', index=False)


#
def update_trade_cal(engine, pro, exh, startDate, endDate, retry_count, pause):
    df = td.get_trade_cal(pro, exh, startDate, endDate, retry_count, pause)
    # df = clean_df_db_dups(df, 'index_daily_basic', engine, dup_cols=['ts_code', 'trade_date'])
    df.to_sql('trade_cal', engine, if_exists='append', index=False)


def update_index_weight_by_date(engine, pro, startDate, endDate, retry_count, pause):
    df = td.get_index_weight_0(pro, startDate,endDate, retry_count, pause)
    df.to_sql('index_weight', engine, if_exists='append', index=False)

def update_index_weight_by_index(engine,pro,indexes,start_date,end_date,retry_count,pause):
    df=pd.DataFrame()
    for code in indexes:
        frame = td.get_index_weight_1(pro,code,start_date,end_date,retry_count,pause)
        print(type(frame))
        if frame is None:
            print(code)
            continue
        if frame.empty:
            print(code)
            continue
        print(frame.head())
        df=df.append(frame,ignore_index=True)
    df.to_sql('index_weight', engine, if_exists='append', index=False)

def clean_df_db_dups(df, tablename, engine, dup_cols=[],
                     filter_continuous_col=None, filter_categorical_col=None):
    """
    Remove rows from a dataframe that already exist in a database
    Required:
        df : dataframe to remove duplicate rows from
        engine: SQLAlchemy engine object
        tablename: tablename to check duplicates in
        dup_cols: list or tuple of column names to check for duplicate row values
    Optional:
        filter_continuous_col: the name of the continuous data column for BETWEEEN min/max filter
                               can be either a datetime, int, or float data type
                               useful for restricting the database table size to check
        filter_categorical_col : the name of the categorical data column for Where = value check
                                 Creates an "IN ()" check on the unique values in this column
    Returns
        Unique list of values from dataframe compared to database table
    """
    args = 'SELECT %s FROM %s' % (', '.join(['"{0}"'.format(col) for col in dup_cols]), tablename)
    args_contin_filter, args_cat_filter = None, None
    if filter_continuous_col is not None:
        if df[filter_continuous_col].dtype == 'datetime64[ns]':
            args_contin_filter = """ "%s" BETWEEN Convert(datetime, '%s')
                                          AND Convert(datetime, '%s')""" % (filter_continuous_col,
                                                                            df[filter_continuous_col].min(),
                                                                            df[filter_continuous_col].max())

    if filter_categorical_col is not None:
        args_cat_filter = ' "%s" in(%s)' % (filter_categorical_col,
                                            ', '.join(["'{0}'".format(value) for value in
                                                       df[filter_categorical_col].unique()]))

    if args_contin_filter and args_cat_filter:
        args += ' Where ' + args_contin_filter + ' AND' + args_cat_filter
    elif args_contin_filter:
        args += ' Where ' + args_contin_filter
    elif args_cat_filter:
        args += ' Where ' + args_cat_filter

    df.drop_duplicates(dup_cols, keep='last', inplace=True)
    df = pd.merge(df, pd.read_sql(args, engine), how='left', on=dup_cols, indicator=True)
    df = df[df['_merge'] == 'left_only']
    df.drop(['_merge'], axis=1, inplace=True)
    return df
