# -*- coding: utf-8 -*-

import time
import datetime
import pandas as pd

"""
Python关于时间的一些知识：
世界标准时间有两个：
GMT时间(格林威治时间)：以前的世界时，本地时间根据时区差异基于GMT进行调整，比如北京时间是东八区，比GMT时间早8小时
（GMT是根据地球自转和公转来计时的，地球自转一圈是一天，绕太阳公转一圈是一年，GMT缺点是地球自转一圈的时间并不是恒定的）
UTC时间：现在世界标准时/世界协调时间，本地时间根据偏移量基于UTC进行调整，比如北京时间偏移量是+0800，即比UTC早8个小时
（UTC时间认为一个太阳日（一天）总是恒定的86400秒（24小时））
时间戳：以某个时间点为基准，按秒为单位计数，通过整数或浮点数来记录时间的方式
UNIX时间戳：以UTC时间1970-01-01 00:00:00为基准的时间戳
本地时间戳：以某个本地时间为基准的时间戳（我们用的北京时间戳通常以北京时间1970-01-01 08:00:00为基准）
对同一个字符时间，转为时间戳时，UTC时间戳比北京时间戳大8*3600
对同一个时间戳，转为为字符时间，UTC时间比北京时间小8小时
time和datetime模块默认时间戳基准是本地（北京）时间1970-01-01 08:00:00
pandas模块默认时间戳基准是UTC时间1970-01-01 00:00:00
参考：
https://mp.weixin.qq.com/s/VdoQt88JfjPJTL9XgohZJQ
https://zhuanlan.zhihu.com/p/412552917
http://t.zoukankan.com/Cheryol-p-13479418.html
https://www.zhihu.com/question/400394490/answer/1273564089
"""

# pandas模块和datetime以及time模块的时间戳有差别（pd多8小时(28800秒)，后两者是一致的）
TSDIF_PD_DTTM = pd.to_datetime('19700102 08:00:00').timestamp() - \
                datetime.datetime(1970, 1, 2, 8, 0, 0).timestamp()
TS_BIAS_DT = (datetime.datetime.fromtimestamp(0) - \
              datetime.datetime.utcfromtimestamp(0)).seconds
    
MONTH_DAYS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6:30, 7: 31,
              8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def _show_time_infos():
    t, t_ns = time.time(), time.time_ns()
    print('原始时间戳:                ', t)
    print('秒级(second, 10位):       ', int(t))
    print('毫秒级(millisecond, 13位):', int(round(t*1000)))
    print('微秒级(microsecond, 16位):', int(round(t*1000000)))
    print('纳秒级(nanosecond, 19位) :', int(round(t*1000000000)))
    print('纳秒级(nanosecond, 19位) :', t_ns)
    
    print('time模块时区名称:', time.tzname)
    print('time模块当前时区时间差:', time.timezone)
    
    fmt = '%Y-%m-%d %H:%M:%S'
    print('time.time()时间戳对应当地时间:',
          time.strftime(fmt, time.localtime(t)))
    print('time.time()时间戳对应UTC时间: ',
          time.strftime(fmt, time.gmtime(t)))
    
    now = time.strftime(fmt)
    print('当前时间pandas datetime时间戳:',
          pd.to_datetime(now).timestamp())
    print('当前时间datetime模块时间戳:    ',
          datetime.datetime.strptime(now, fmt).timestamp())
    print('当前时间time模块时间戳:        ',
          time.mktime(time.strptime(now, fmt)))
    
    print('pandas datetime时间戳起始时间:', pd.to_datetime(0))
    print('datetime模块时间戳起始时间:    ', datetime.datetime.fromtimestamp(0))
    print('time模块时间戳起始时间(当地):   ', time.strftime(fmt, time.localtime(0)))
    print('time模块时间戳起始时间(UTC):   ', time.strftime(fmt, time.gmtime(0)))
