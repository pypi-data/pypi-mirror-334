# -*- coding: utf-8 -*-

import time
import datetime
import pandas as pd
try:
    from .dtconst import TS_BIAS_DT, TSDIF_PD_DTTM
except:
    from dramkit.dttools.dtconst import TS_BIAS_DT, TSDIF_PD_DTTM


def pd_str2datetime(o, **kwargs):
    """pd.to_datetime函数封装，排除o为时间戳（统一按str处理）"""
    if type(o).__name__ in ['Series', 'ndarray']:
        try:
            return pd.to_datetime(o.astype(int).astype(str), **kwargs)
        except:
            try:
                return pd.to_datetime(o.astype(str), **kwargs)
            except:
                return pd.to_datetime(o, **kwargs)
    else:
        try:
            return pd.to_datetime(str(o), **kwargs)
        except:
            try:
                return pd.to_datetime(str(int(o)), **kwargs)
            except:
                return pd.to_datetime(o, **kwargs)
            
            
def datetime2str(dt, strformat=None, tz='local'):
    """
    datatime格式转为str格式
    
    Parameters
    ----------
    dt : datetime.datetime, datetime.date, time.struct_time, pd.Timestamp
        datetime、time或pandas格式时间
    strformat : None, bool, str
        设置返回文本格式：
        
        - False, 直接返回dt
        - 'timestamp', 返回timestamp
        - 'int', 返回int格式日期，如'20221106'
        - None, 默认'%Y-%m-%d %H:%M:%S'格式        
        - 指定其他文本格式
    tz : str
        指定时区，可选['local', 'utc']
        
    Examples
    --------
    >>> dt1, dt2 = datetime.datetime.now(), time.localtime()
    >>> dt3 = pd_str2datetime(datetime_now())
    >>> datetime2str(dt1, 'timestamp', 'utc')
    >>> datetime2str(dt2, 'timestamp', 'utc')
    >>> datetime2str(dt3, 'timestamp', 'utc')
    >>> dt4 = time.gmtime()
    >>> datetime2str(dt3, 'timestamp', 'utc')
    >>> datetime2str(dt3, 'timestamp')
    """
    if strformat == False:
        return dt
    if strformat is None:
        # strformat = '%Y-%m-%d %H:%M:%S.%f' # 到微秒
        strformat = '%Y-%m-%d %H:%M:%S' # 到秒
        # strformat = '%Y-%m-%d' # 到日
    dt_type = type(dt).__name__
    assert dt_type in ['datetime', 'date', 'Timestamp', 'struct_time']
    assert tz in ['local', 'utc']
    if strformat == 'int':
        try:
            return int(dt.strftime('%Y%m%d'))
        except:
            return int(time.strftime('%Y%m%d', dt))
    elif strformat == 'timestamp':
        if dt_type in ['datetime', 'date']:
            if tz == 'local':
                return dt.timestamp()
            else:
                return dt.timestamp() + TS_BIAS_DT
        elif dt_type == 'struct_time':
            if tz == 'local':
                return time.mktime(dt)
            else:
                return time.mktime(dt) - time.timezone
        else:
            if tz == 'local':
                return dt.timestamp() - TSDIF_PD_DTTM
            else:
                return dt.timestamp()
    else:
        try:
            try:
                res = dt.strftime(strformat)
            except:
                res = time.strftime(strformat, dt)
            if res == strformat:
                raise
            if not pd.isna(pd_str2datetime(res, format=strformat)):
                return res
            raise
        except:
            if dt_type == 'struct_time':
                return time.strftime('%Y-%m-%d %H:%M:%S.%f', dt)
            else:
                return str(dt)
            
            
def dtseries2str(series, joiner='-', strformat=None):
    """pd.Series转化为str，若不指定strformat，则按joiner连接年月日"""
    res = pd.to_datetime(series)
    if pd.isnull(strformat):
        strformat = '%Y{x}%m{x}%d'.format(x=joiner)
    res = res.apply(lambda x: x.strftime(strformat))
    return res


def check_dt_format(dt, strformat='%Y%m%d'):
    """检查dt的格式是否符合strformat"""
    try:
        dt = datetime.datetime.strptime(dt, strformat)
        return True
    except:
        return False


def get_datetime_strformat(tstr,
                           ymd = ['-', '', '.', '/'],
                           ymd_hms = [' ', '', '.'],
                           hms = [':', ''],
                           hms_ms = ['.', '']
                           ):
    """
    | 获取常用的文本时间格式format，支持包含以下几个部分的时间类型：
    | 年月日、年月日时分秒、年月日时分、年月日时分秒毫秒、年月日时、年月
    
    TODO
    ----
    改为用正则表达式匹配（根据连接符、数字占位限制和数字大小限制来匹配）
    
    Parameters
    ----------
    ymd : list
        年月日连接符
    ymd_hms : list
        年月日-时分秒连接符
    hms : list
        时分秒连接符
    hms_ms : list
        时分秒-毫秒连接符
    """
    assert isinstance(tstr, str), '只接受文本格式时间！'
    for j1 in ymd:
        try:
            # 年月日
            fmt1 = '%Y{j1}%m{j1}%d'.format(j1=j1)
            _ = time.strptime(tstr, fmt1)
            if len(tstr) == 8+2*len(j1):
                return fmt1
            else:
                raise
        except:
            for j2 in ymd_hms:
                for j3 in hms:
                    try:
                        # 年月日时分秒
                        fmt2 = fmt1 + '{j2}%H{j3}%M{j3}%S'.format(j2=j2, j3=j3)
                        _ = time.strptime(tstr, fmt2)
                        if len(tstr) == 14+2*len(j1)+len(j2)+2*len(j3):
                            return fmt2
                        else:
                            raise
                    except:
                        try:
                            # 年月日时分
                            fmt21 = fmt1 + '{j2}%H{j3}%M'.format(j2=j2, j3=j3)
                            _ = time.strptime(tstr, fmt21)
                            if len(tstr) == 12+2*len(j1)+len(j2)+len(j3):
                                return fmt21
                            else:
                                raise
                        except:
                            for j4 in hms_ms:
                                try:
                                    # 年月日时分秒毫秒
                                    fmt3 = fmt2 + '{j4}%f'.format(j4=j4)
                                    _ = time.strptime(tstr, fmt3)
                                    if len(tstr) > 14+2*len(j1)+len(j2)+2*len(j3)+len(j4):
                                        len1 = 14+2*len(j1)+len(j2)+2*len(j3)
                                        tstr1 = tstr[:len1]
                                        _ = time.strptime(tstr1, fmt2)
                                        if len(tstr1) == len1:
                                           return fmt3
                                        else:
                                            raise
                                    else:
                                        raise
                                except:
                                    try:
                                        # 年月日时
                                        fmt22 = fmt1 + '{j2}%H'.format(j2=j2)
                                        _ = time.strptime(tstr, fmt22)
                                        if len(tstr) == 10+2*len(j1)+len(j2):
                                            return fmt22
                                        else:
                                            raise
                                    except:
                                        try:
                                            # 年月
                                            fmt11 = '%Y{j1}%m'.format(j1=j1)
                                            _ = time.strptime(tstr, fmt11)
                                            if len(tstr) == 6+len(j1):
                                                return fmt11
                                            else:
                                                raise
                                        except:
                                            pass
    raise ValueError('未识别的日期时间格式！')
    
    
def str2datetime(tstr, strformat=None):
    """时间字符串转datetime格式"""
    return pd.to_datetime(tstr, format=strformat)
    # if strformat is None:
    #     strformat = get_datetime_strformat(tstr)
    # return pd.to_datetime(tstr, format=strformat)
    
    
def str2timestamp(t, strformat=None, tz='local'):
    """
    | 时间字符串转时间戳
    | 若大于16位(纳秒级)，返回string，否则返回float(毫秒级)
    """
    assert tz in ['local', 'utc']
    t = str2datetime(t, strformat=strformat)
    ts = t.timestamp()
    if tz == 'local':
        ts = ts - TSDIF_PD_DTTM
    if t.nanosecond > 0:
        ts = str(ts) + str(t.nanosecond)
    return ts
    
    
def timestamp2str(t, strformat=None, tz='local', method=2):
    """    
    | 时间戳转化为字符串格式
    | 注意：t小于0时直接按t为秒数处理（即使整数部分超过10位也不会处理为小数）
    """
    assert tz in ['local', 'utc']
    assert method in [1, 2, 3] # 经测试method=2速度最快
    assert isinstance(t, (int, float, str)), '请检查时间戳格式！'
    assert isinstance(strformat, (type(None), str)), '请指定正确的输出格式！'
    strformat = '%Y-%m-%d %H:%M:%S' if strformat is None else strformat
    def _delta2str(seconds):
        if tz == 'local':
            tbase = datetime.datetime.fromtimestamp(0)
        else:
            tbase = datetime.datetime.utcfromtimestamp(0)
        dt = tbase + datetime.timedelta(seconds=seconds)
        return dt.strftime(strformat)        
    # t小于0特殊处理
    if float(t) < 0:
        return _delta2str(float(t))
    # 先转化为时间戳数字（整数部分大于10位的转化为小数）
    ts = str(t).replace('.', '')
    if len(ts) > 10:
        part_int = ts[:10]
        part_float = ts[10:]
        ts = int(part_int) + int(part_float) / (10**len(part_float))
    else:
        ts = float(t)
    # 方式一：用datetime.fromtimestamp
    if method == 1:
        if tz == 'local':
            dt = datetime.datetime.fromtimestamp(ts)
        else:
            dt = datetime.datetime.utcfromtimestamp(ts)
        return dt.strftime(strformat)
    # 方式二：用time.localtime
    if method == 2:
        if tz == 'local':
            dt = time.localtime(ts)
        else:
            dt = time.gmtime(ts)
        return time.strftime(strformat, dt)
    # 方式三：用timedelta转化
    if method == 3:
        return _delta2str(ts)

    
def get_datetime_format(dt,
                        ymd = ['-', '', '.', '/'],
                        ymd_hms = [' ', '', '.'],
                        hms = [':', ''],
                        hms_ms = ['.', '']
                        ):
    """
    | 获取常用日期时间格式format
    | 注：整数和浮点数都可能是时间戳，这里以常用的规则来判断：
    |    - 若整数长度为8位，判断为整数型日期
    |    - 若整数或浮点数长度不小于10位不大于19位，判断为时间戳
    |    - 其他情况下的整数或浮点数报错处理
    """
    dt_type = type(dt).__name__
    if dt_type in ['datetime', 'date']:
        return 'datetime.' + dt_type, None
    if dt_type == 'Timestamp':
        return 'pd.' + dt_type, None
    if dt_type == 'struct_time':
        return 'time.' + dt_type, None
    if isinstance(dt, (int, float, str)):
        try:
            fmt = get_datetime_strformat(str(dt), ymd=ymd,
                                         ymd_hms=ymd_hms,
                                         hms=hms, hms_ms=hms_ms)
            return type(dt).__name__, fmt
        except:
            try:
                _ = float(dt)
                if 10 <= len(str(dt)) <= 19:
                    return type(dt).__name__, 'timestamp'
            except:
                pass
    raise ValueError('未识别的日期时间格式！')
    
    
def x2datetime(x, tz='local'):
    """
    | x转化为datetime格式，若x为timestamp，应设置时区tz
    | 若x为8位整数，则转化为str处理，其余情况直接用用pd.to_datetime处理
    """
    if isinstance(x, time.struct_time):
        return pd.to_datetime(
               datetime.datetime.fromtimestamp(time.mktime(x)))
    elif isinstance(x, int) and len(str(x)) == 8:
        return pd.to_datetime(str(x))
    else:
        try:
            xtype, fmt = get_datetime_format(x)
            if fmt == 'timestamp':
                return pd.to_datetime(timestamp2str(x, tz=tz))
            else:
                return pd.to_datetime(x)
        except:
            return pd.to_datetime(x)


def copy_format(to_tm, from_tm):
    """
    复制日期时间格式
    """
    if pd.isna(from_tm):
        return to_tm
    input_type = type(to_tm).__name__
    types1 = ['datetime', 'date', 'Timestamp', 'struct_time']
    types2 = ['str', 'int', 'float']
    types3 = ['ndarray', 'Series', 'list', 'tuple']
    assert input_type in types1+types2+types3
    if input_type == type(from_tm).__name__ and input_type in types1:
        return to_tm
    onlyone = False
    if not input_type in types3:
        onlyone = True
        to_tm = [to_tm]
    if len(to_tm) == 0:
        return to_tm
    def _return(res):
        if onlyone:
            return res[0]
        return res
    tz = 'local'
    res = [x2datetime(x, tz=tz) for x in to_tm]
    dtype, fmt = get_datetime_format(from_tm)
    if fmt is None:
        if dtype == 'time.struct_time':
            res = [x.timetuple() for x in res]
        elif dtype == 'datetime.date':
            res = [datetime.date(x.year, x.month, x.day) for x in res]
        elif dtype == 'datetime.datetime':
            res = [datetime.datetime.fromtimestamp(x.timestamp()-TSDIF_PD_DTTM) \
                   for x in res]
        return _return(res)
    if fmt == 'timestamp':
        # TODO: 不同格式的timestamp处理（如10位，13位，整数，小数等）
        res = [datetime2str(x, strformat='timestamp', tz=tz) for x in res]
        return _return(res)
    res = [x.strftime(fmt) for x in res]
    if dtype in ['int', 'float']:
        res = [eval('%s(x)'%dtype) for x in res]
    return _return(res)


def copy_format0(to_tm, from_tm):
    """
    | 复制日期时间格式
    | 若from_tm是日期时间格式或时间戳格式，则直接返回to_tm
    """
    dtype, fmt = get_datetime_format(from_tm)
    if fmt in [None, 'timestamp']:
        return to_tm
    input_type = type(to_tm).__name__
    types1 = ['datetime', 'date', 'Timestamp', 'struct_time']
    types2 = ['ndarray', 'Series', 'list', 'tuple']
    assert input_type in types1+types2
    onlyone = False
    if not input_type in types2:
        onlyone = True
        to_tm = [to_tm]
    if len(to_tm) == 0:
        return to_tm                        
    dt_type = type(to_tm[0]).__name__
    assert dt_type in ['datetime', 'date', 'Timestamp', 'struct_time']
    if dt_type == 'struct_time':
        res = [time.strftime(fmt, x) for x in to_tm]
    else:
        res = [x.strftime(fmt) for x in to_tm]
    if dtype in ['int', 'float']:
        res = [eval('%s(x)'%dtype) for x in res]
    if onlyone:
        res = res[0]
    return res
