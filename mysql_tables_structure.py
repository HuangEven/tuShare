# coding=utf-8

from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockBasic(Base):
    """股票列表
    is_hs	    str	N	是否沪深港通标的，N否 H沪股通 S深股通
    list_status	str	N	上市状态： L上市 D退市 P暂停上市
    exchange	str	N	交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
    """
    __tablename__ = 'stock_basic'

    ts_code = Column(String(10), primary_key=True)  # TS代码
    symbol = Column(String(10))         # 股票代码
    name = Column(String(10))           # 股票名称
    area = Column(String(4))            # 所在地域
    industry = Column(String(4))        # 所属行业
    fullname = Column(String(30))       # 股票全称
    enname = Column(String(100))        # 英文全称
    market = Column(String(3))          # 市场类型 （主板/中小板/创业板）
    exchange = Column(String(4))        # 交易所代码
    curr_type = Column(String(3))       # 交易货币
    list_status = Column(String(1))     # 上市状态： L上市 D退市 P暂停上市
    list_date = Column(String(8))       # 上市日期
    delist_date = Column(String(8))     # 退市日期
    is_hs = Column(String(1))           # 是否沪深港通标的，N否 H沪股通 S深股通

# 创建“日线行情”表结构
class Daily(Base):
    """日线行情
    ts_code	str	N	股票代码（二选一）
    trade_date	str	N	交易日期（二选一）
    start_date	str	N	开始日期(YYYYMMDD)
    end_date	str	N	结束日期(YYYYMMDD)
    """
    __tablename__ = 'daily'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    trade_date = Column(String(8), primary_key=True)    # 交易日期
    open = Column(Float)        # 开盘价
    high = Column(Float)        # 最高价
    low = Column(Float)         # 最低价
    close = Column(Float)       # 收盘价
    pre_close = Column(Float)   # 昨收价
    change = Column(Float)      # 涨跌额
    pct_chg = Column(Float)     # 涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
    vol = Column(Float)         # 成交量 （手）
    amount = Column(Float)      # 成交额 （千元）


# 个股每日指标
class DailyBasic(Base):
    """
    日线行情数据中已有收盘价，每日指标表中不保存收盘价
    股息率dv_ratio、da_ttm等存在空值，用0值填充
    """
    __tablename__='daily_basic'

    ts_code = Column(String(10), primary_key=True)      # 股票代码
    trade_date = Column(String(8), primary_key=True)    # 交易日期
    close = Column(Float)   # 当日收盘价
    turnover_rate = Column(Float)   # 换手率（%）
    turnover_rate_f = Column(Float)     # 换手率（自由流通股）
    volume_ratio = Column(Float)    # 量比
    pe = Column(Float)      # 市盈率（总市值/净资产）
    pe_ttm = Column(Float)  # 市盈率（TTM）
    pb = Column(Float)      # 市净率（总市值/净资产）
    ps = Column(Float)  # 市销率
    ps_ttm = Column(Float)  # 市销率（TTM）
    dv_ratio = Column(Float)    # 股息率（%）
    dv_ttm = Column(Float)  # 股息率（TTM）（%）
    total_share = Column(Float)     # 总股本（万股）
    float_share = Column(Float)     # 流通股本（万股）
    free_share = Column(Float)      # 自由流通股本（万）
    total_mv = Column(Float)        # 总市值（万元）
    circ_mv = Column(Float)         # 流通市值（万元）


# 指数日线行情
class IndexDaily(Base):
    __tablename__ = 'index_daily'

    ts_code = Column(String(10), primary_key=True)      # TS指数代码
    trade_date = Column(String(8), primary_key=True)    # 交易日
    close = Column(Float)       # 收盘点位
    open = Column(Float)    # 开盘点位
    high = Column(Float)    # 最高点位
    low = Column(Float)     # 最低点位
    pre_close = Column(Float)   # 昨日收盘点
    change = Column(Float)      # 涨跌点
    pct_chg = Column(Float)     # 涨跌幅（%）
    vol = Column(Float)     # 成交量（手）
    amount = Column(Float)  # 成交额（千元）


# 指数每日指标
class IndexDailyBasic(Base):
    __tablename__ = 'index_daily_basic'

    ts_code = Column(String(10), primary_key=True)      # TS指数代码
    trade_date = Column(String(8), primary_key=True)    # 交易日
    total_mv = Column(Float)    # 当日总市值（元）
    float_mv = Column(Float)    # 当日流通市值（元）
    total_share = Column(Float)     # 当日总股本（股）
    float_share = Column(Float)     # 当日流通股本（股）
    free_share = Column(Float)  # 当日自由流通股本（股）
    turnover_rate = Column(Float)  # 换手率
    turnover_rate_f = Column(Float)    #换手率（基于自由流通股本）
    pe = Column(Float)      # 市盈率
    pe_ttm = Column(Float)  # 市盈率（TTM）
    pb = Column(Float)      # 市净率


# 交易日历
class TradeCal(Base):
    __tablename__ = 'trade_cal'

    exchange = Column(String(5), primary_key=True)
    cal_date = Column(String(8), primary_key=True)
    is_open = Column(String(1))
    pretrade_date = Column(String(8))


# 指数基本信息
class IndexBasic(Base):
    __tablename__ = 'index_basic'

    ts_code = Column(String(20), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(100))
    market = Column(String(8))
    publisher = Column(String(20))
    index_type = Column(String(100))
    category = Column(String(10))
    base_date = Column(String(10))
    base_point = Column(String(10))
    list_date = Column(String(10))
    weight_rule = Column(String(20))
    desc = Column(String(2000))
    exp_date = Column(String(10))


# 指数成分
class IndexWeight(Base):
    __tablename__ = 'index_weight'

    index_code = Column(String(10), primary_key=True)
    con_code = Column(String(10), primary_key=True)
    trade_date = Column(String(8), primary_key=True)
    weight = Column(Float)

