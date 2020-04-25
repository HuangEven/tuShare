# !/usr/bin/env python
# -*- coding:utf-8 -*-
# coding=utf-8

import time
import pandas as pd
import get_date as gtd


def get_stock_basic(pro, retry_count=3, pause=2):
    """股票列表 数据"""
    frame = pd.DataFrame()
    for status in ['L', 'D', 'P']:
        for _ in range(retry_count):
            try:
                df = pro.stock_basic(exchange='', list_status=status,
                                     fields='ts_code,symbol,name,area,industry,fullname,enname,market, \
                                    exchange,curr_type,list_status,list_date,delist_date,is_hs')
            except:
                time.sleep(pause)
            else:
                frame = frame.append(df)
                break

    return frame


def get_daily_code(pro, ts_code, date, retry_count=3, pause=2):
    """股票代码方式获取 日线行情 数据"""
    for _ in range(retry_count):
        try:
            df = pro.daily(ts_code=ts_code, trade_date=date,
                           fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        except:
            time.sleep(pause)
        else:
            return df


def get_daily_date(pro, date, retry_count=3, pause=2):
    """日期方式获取 日线行情 数据"""
    for _ in range(retry_count):
        try:
            df = pro.daily(trade_date=date,
                           fields='ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount')
        except:
            time.sleep(pause)
        else:
            return df


def get_daily_basic_date(pro, date, retry_count=3, pause=2):
    """日期方式获取 每日指标 数据"""
    for _ in range(retry_count):
        try:
            df = pro.daily_basic(ts_code='', trade_date=date,
                                 fields='ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,'
                                        'pe,pe_ttm, pb,ps,ps_ttm,dv_ratio,dv_ttm,total_share,float_share,'
                                        'free_share,total_mv,circ_mv')
        except:
            time.sleep(pause)
        else:
            return df


def get_index_daily_date(pro, code, startDate, endDate, retry_count=3, pause=2):
    """日期方式获取 大盘日线行情 数据"""
    for _ in range(retry_count):
        try:
            df = pro.index_daily(ts_code=code, start_date=startDate, end_date=endDate)
        except:
            time.sleep(pause)
        else:
            return df


def get_index_daily_basic_date(pro, startDate, endDate, retry_count=3, pause=2):
    """日期方式获取 每日大盘指标 数据"""
    for _ in range(retry_count):
        try:
            df = pro.index_dailybasic(ts_code='', start_date=startDate, end_date=endDate,
                                      fields='trade_date,ts_code,total_mv,float_mv,total_share,'
                                             'float_share,free_share,turnover_rate,turnover_rate_f,pe,pe_ttm,pb')
        except:
            time.sleep(pause)
        else:
            return df


def get_trade_cal(pro, exh, startDate, endDate, retry_count=3, pause=2):
    for _ in range(retry_count):
        try:
            df = pro.trade_cal(exchange=exh, start_date=startDate, end_date=endDate,
                               fields='exchange,cal_date,is_open,pretrade_date')
        except:
            time.sleep(pause)
        else:
            return df


def get_index_basic(pro, market, retry_count=3, pause=2):
    for _ in range(retry_count):
        try:
            df = pro.index_basic(market=market,
                                 fields='ts_code,name,fullname,market,publisher,index_type,category,base_date,base_point,list_date,weight_rule,desc,exp_date')
        except:
            time.sleep(pause)
        else:
            return df


def get_index_weight_0(pro, start_date, end_date, retry_count=3, pause=2):
    # date_list=gtd.get_date_list(start_date,end_date)
    for _ in range(retry_count):
        try:
            df = pro.index_weight(start_date=start_date, trade_date=end_date)
        except:
            time.sleep(pause)
        else:
            return df


def get_index_weight_1(pro, code, start_date,end_date,retry_count=3, pause=2):
    for _ in range(retry_count):
        try:
            df = pro.index_weight(index_code=code,start_date=start_date,end_date=end_date)
        except:
            time.sleep(pause)
        else:
            return df
