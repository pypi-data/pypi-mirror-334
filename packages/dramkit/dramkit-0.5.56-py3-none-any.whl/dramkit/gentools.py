# -*- coding: utf-8 -*-

'''
General toolboxs
'''

import argparse
import copy
import datetime
import inspect
import logging
import operator
import re
import string
import os
import sys
import time
import warnings
import traceback
import urllib.parse
from collections import Counter
from collections.abc import Callable, Iterable
from functools import reduce, wraps
from io import StringIO
from itertools import product
from random import randint, random, uniform
from beartype import beartype
from beartype.typing import List, Tuple, Any, NewType, Union
from dramkit.const import PY_VERSION2, SeriesType
if PY_VERSION2 >= '03.08.00':
    from typing import Literal
else:
    from typing_extensions import Literal

import numpy as np
import pandas as pd
from tqdm import tqdm

from dramkit.logtools.utils_logger import logger_show
from dramkit.speedup.multi_thread import SingleThread

PYTHON_VERSION = '.'.join([x.zfill(2) for x in sys.version.split(' ')[0].split('.')])


class TimeRecoder(object):
    '''
    运行时间记录器
    
    Examples
    --------
    >>> tr = TimeRecoder()
    >>> time.sleep(5)
    >>> tr.useds()
    >>> time.sleep(60)
    >>> tr.usedm()
    >>> time.sleep(5)
    >>> tr.used()
    '''
    
    def __init__(self, monotonic=False, logger=None):
        self.monotonic = monotonic
        self.strt_tm = self.now()
        self.end_tm = None
        self.logger = logger
        
    def _check_logger(self, logger=None):
        if isnull(logger):
            return self.logger
        return logger
        
    def now(self):
        if self.monotonic:
            return time.monotonic()
        else:
            return time.time()
        
    def used(self, logger=None):
        self.end_tm = self.now()
        s = self.end_tm - self.strt_tm
        if s < 60:
            s = round(s, 6)
            logger_show('used time: %ss.'%s, self._check_logger(logger))
        elif s < 3600:
            m, s = divmod(s, 60)
            logger_show('used time: %sm, %ss.'%(m, round(s, 2)),
                        self._check_logger(logger))
        else:
            h, s = divmod(s, 3600)
            m, s = divmod(s, 60)
            logger_show('used time: %sh, %sm, %ss.'%(h, m, round(s, 2)),
                        self._check_logger(logger))
        return s
    
    def useds(self, logger=None):
        self.end_tm = self.now()
        s = round(self.end_tm-self.strt_tm, 6)
        logger_show('used time: %ss.'%s, self._check_logger(logger))
        return s
        
    def usedm(self, logger=None):
        self.end_tm = self.now()
        s = self.end_tm - self.strt_tm
        m = round(s/60, 6)
        logger_show('used time: %sm.'%m, self._check_logger(logger))
        return s


class GenObject(object):
    '''
    | 创建一个数据类型，用于存放变量值，
    | 既可以用.key调用，也可以像字典一样调用[key]调用
    '''

    def __init__(self, dirt_modify=True, **kwargs):
        '''初始化'''
        self.set_dirt_modify(dirt_modify)
        self.set_from_dict(kwargs)
        
    @property
    def dirt_modify(self):
        return self.__dirt_modify
        
    def set_dirt_modify(self, dirt_modify):
        assert isinstance(dirt_modify, bool)
        self.__dirt_modify = dirt_modify
        
    def __setattr__(self, key, value):
        _defaults = ['__dirt_modify']
        _defaults = ['_%s'%type(self).__name__ + x for x in _defaults]
        if key in _defaults:
            self.__dict__[key] = value
            return
        if self.dirt_modify:
            self.__dict__[key] = value
        else:
            # raise_error('DirtModifyError', '不允许直接赋值！')
            raise_error('DirtModifyError', '不允许直接赋值，请调用`set_key_value`或`set_from_dict`方法！')

    def __repr__(self):
        '''查看时以key: value格式打印'''
        _defaults = ['__dirt_modify']
        _defaults = ['_%s'%type(self).__name__ + x for x in _defaults]
        return ''.join('{}: {}\n'.format(k, v) for k, v in self.__dict__.items() \
                       if k not in _defaults)
            
    def __getitem__(self, key):
        '''像dict一样通过key获取value'''
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        '''像dict一样直接通过key赋值'''
        self.__setattr__(key, value)
            
    @property
    def keys(self):
        '''显示所有key'''
        _defaults = ['__dirt_modify']
        _defaults = ['_%s'%type(self).__name__ + x for x in _defaults]
        # return [x for x in self.__dict__.keys() if x not in _defaults]
        for x in self.__dict__.keys():
             if x not in _defaults:
                yield x
                
    def listkeys(self):
        return list(self.keys)
    
    @property
    def items(self):
        _defaults = ['__dirt_modify']
        _defaults = ['_%s'%type(self).__name__ + x for x in _defaults]
        for x in self.__dict__.keys():
            if not x in _defaults:
                d = (x, eval('self.{}'.format(x)))
                yield d
                
    def listitems(self):
        return list(self.items)
    
    def set_key_value(self, key, value, note=None):
        self.__dict__[key] = value
        if not isna(note):
            self.__dict__['%s_note'%key] = note
            
    def set_note(self, key, note):
        self.set_key_value('%s_note'%key, note)
    
    def set_from_dict(self, d):
        '''通过dict批量增加属性变量'''
        assert isinstance(d, dict), '必须为dict格式'
        self.__dict__.update(d)
        
    def update(self, o):
        '''像dict一样通过update函数传入字典进行更新'''
        assert isinstance(o, (dict, list, tuple, type(self)))
        if isinstance(o, dict):
            self.set_from_dict(o)
        else:
            self.merge(o)
        
    def merge(self, o):
        '''从另一个对象中合并属性和值'''
        assert isinstance(o, (list, tuple, type(self)))
        if isinstance(o, type(self)):
            o = [o]
        assert all([isinstance(x, type(self)) for x in o])
        for x in o:
            for key in x.keys:
                exec('self.set_key_value(key, x.{})'.format(key))
    
    def copy(self):
        return copy.deepcopy(self)
    
    def pop(self, key):
        '''删除属性变量key，有返回'''
        return self.__dict__.pop(key)

    def remove(self, key):
        '''删除属性变量key，无返回'''
        del self.__dict__[key]

    def clear(self):
        '''清空所有属性变量'''
        self.__dict__.clear()
        
        
class StructureObject(object):
    def __init__(self, *args, **kwargs):
        raise_error('DeprecatedError', '`StructureObject`已弃用，请调用`GenObject`!')
        
        
class GenClass(object):
    '''通用类'''
    
    def __init__(self, *args, **kwargs):
        attrs = locals().copy()
        kwargs = attrs.pop('kwargs')
        attrs.update(kwargs)
        self.set_params(attrs)

    def set_params(self, params_dict: dict):
        '''设置或修改属性'''
        if 'logger' in params_dict:
            logger = params_dict.pop('logger')
            self.logger = logger
        for k, v in params_dict.items():
            if not k == 'self':
                self.__dict__[k] = v

        
def run_func_with_timeout_thread(func, *args,
                                 timeout=10,
                                 logger_error=False,
                                 logger_timeout=None,
                                 timeout_show_str=None,
                                 kill_when_timeout=True,
                                 **kwargs):
    '''
    | 限定时间(timeout秒)执行函数func，若限定时间内未执行完毕，返回None
    | args为tuple或list，为func函数接受的参数列表
    
    | 注：在线程中强制结束函数可能导致未知错误，
    | 比如文件资源打开了但是强制结束时不能关闭
    '''
    # 创建线程
    task = SingleThread(func, args, kwargs,
                        logger=logger_error,
                        # daemon=True
                        )
    task.start() # 启动线程
    task.join(timeout=timeout) # 最大执行时间
    # 超时处理
    if task.is_alive():
        if not isnull(timeout_show_str):
            logger_show(timeout_show_str, logger_timeout, 'warn')
        # 强制结束
        if kill_when_timeout:
            task.stop_thread()
            # task.join()
    return task.get_result()


def with_timeout_thread(timeout=30,
                        logger_error=None,
                        logger_timeout=None,
                        timeout_show_str=None,
                        kill_when_timeout=True):
    '''
    | 作为装饰器在指定时间timeout(秒)内运行函数，超时则结束运行
    | 通过控制线程实现

    Examples
    --------
    .. code-block:: python
        :linenos:

        import os
        import pandas as pd
        from dramkit.gentools import tmprint
        
        df1 = pd.DataFrame([[1, 2], [3, 4]])
        df2 = pd.DataFrame([[5, 6], [7, 8]])
        df1.to_excel('./_test/with_timeout_thread_test_df.xlsx')
        TIMEOUT = 3
        
        @with_timeout_thread(TIMEOUT,
                             logger_error=False
                             )
        def func(x):
            with open('./_test/with_timeout_thread_test_df.xlsx') as f:
                tmprint('sleeping...')
                time.sleep(5)
            df2.to_excel('./_test/with_timeout_thread_test_df.xlsx')
            return x
        
        def test():
            res = func('test')
            print('res:', res)
            os.remove('./_test/with_timeout_thread_test_df.xlsx')
            return res
            
    >>> res = test()
    '''
    def transfunc(func):
        @wraps(func)
        def timeouter(*args, **kwargs):
            '''尝试在指定时间内运行func，超时则结束运行'''
            return run_func_with_timeout_thread(
                    func, *args, timeout=timeout, 
                    logger_error=logger_error,
                    logger_timeout=logger_timeout,
                    timeout_show_str=timeout_show_str,
                    kill_when_timeout=kill_when_timeout,
                    **kwargs)
        return timeouter
    return transfunc


def __chose_logger(logger, kwargs):
    if isnull(logger) and 'logger' in kwargs:
        return kwargs['logger']
    return logger
        
        
def try_repeat_run(n_max_run=3,
                   logger=None,
                   sleep_seconds=0,
                   force_rep=False):
    '''
    | 作为装饰器尝试多次运行指定函数
    | 使用场景：第一次运行可能出错，需要再次运行(比如取数据时第一次可能连接超时，需要再取一次)
    
    Parameters
    ----------
    n_max_run : int
        最多尝试运行次数
    logger : None, logging.Logger
        日志记录器
    sleep_seconds : int, float
        | 多次执行时，上一次执行完成之后需要暂停的时间（秒）
        | 注：在force_rep为True时，每次执行完都会暂停，force_rep为False只有报错之后才会暂停
    force_rep : bool
        若为True，则不论是否报错都强制重复执行，若为False，则只有报错才会重复执行
        
    Returns
    -------
    result : None, other
        若目标函数执行成功，则返回执行结果；若失败，则返回None

    Examples
    --------
    .. code-block:: python
        :linenos:

        from dramkit import simple_logger
        logger = simple_logger()
        
        @try_repeat_run(2, logger=logger, sleep_seconds=0, force_rep=False)
        def rand_div(x):
            return x / np.random.randint(-1, 1)

        def repeat_test(info_):
            print(info_)
            return rand_div(0)

    >>> a = repeat_test('repeat test...')
    >>> print(a)
    '''
    def transfunc(func):
        @wraps(func)
        def repeater(*args, **kwargs):
            '''尝试多次运行func'''
            logger_ = __chose_logger(logger, kwargs)
            if not force_rep:
                n_run, ok = 0, False
                while not ok and n_run < n_max_run:
                    n_run += 1
                    # logger_show('第%s次运行`%s`...'%(n_run, func.__name__),
                    #             logger_, 'info')
                    try:
                        result = func(*args, **kwargs)
                        return result
                    except:
                        if n_run == n_max_run:
                            logger_show(traceback.format_exc(), logger_)
                            logger_show('`%s`运行失败，共运行了%s次。'%(func.__name__, n_run),
                                        logger_, 'error')                            
                            return
                        else:
                            if sleep_seconds > 0:
                                time.sleep(sleep_seconds)
                            else:
                                pass
            else:
                n_run = 0
                while n_run < n_max_run:
                    n_run += 1
                    try:
                        result = func(*args, **kwargs)
                        logger_show('`%s`第%s运行：成功。'%(func.__name__, n_run),
                                    logger_, 'info')
                    except:
                        logger_show(traceback.format_exc(), logger_)
                        logger_show('`%s`第%s运行：失败。'%(func.__name__, n_run),
                                    logger_, 'error')
                        result = None
                    if sleep_seconds > 0:
                        time.sleep(sleep_seconds)
                return result
        return repeater
    return transfunc


def get_caller_pos_info(stacklevel: int):
    """获取调用此函数的语句来源于哪个Python脚本的哪一行
    """
    tgt = traceback.extract_stack()[-int(stacklevel)]
    fname, lineno, line = tgt.filename, tgt.lineno, tgt.line
    return fname, lineno, line


def read_nlines(fpath, n, encoding=None,
                random_seed=False,
                logger=None, **kwargs_open):
    """读取文本文件中的指定数量的行
    
    TODO
    ----
    随机取指定数量的行，random_seed为False时按顺序取，否则随机取

    Parameters
    ----------
    fpath : str
        待读取文件路径
    n : int
        需要读取的行数
    encoding : str, None
        文件编码格式，若不指定，则尝试用utf-8和gbk编码读取
    logger : None, logging.Logger
        日志记录器


    :returns: `list` - 文本文件中每行内容列表
    """
    ens = [encoding] + list({'utf-8', None, 'gbk'}-{encoding})
    for en in ens:
        try:
            with open(fpath, 'r', encoding=en, **kwargs_open) as f:
                k = 0
                lines = []
                for line in f:
                    lines.append(line)
                    k += 1
                    if k >= n:
                        break
                return lines
        except:
            pass
    if os.path.exists(fpath):
        logger_show('未正确识别文件编码格式，以二进制读取: %s'%fpath,
                    logger, 'warn')
    with open(fpath, 'rb', **kwargs_open) as f:
        k = 0
        lines = []
        for line in f:
            lines.append(line)
            k += 1
            if k >= n:
                break
        return lines
    return lines


def raise_warn(name: str,
               msg: str,
               code: Union[int, str] = None,
               can_catch: bool = True,
               **kwargs):
    """抛出警告, name警告名称、msg警告信息、code警告代码、logger日志记录器
    
    Examples
    --------
    >>> from dramkit import simple_logger
    >>> logger = simple_logger('./_test/test_raise_warn.log', 'a')    
    >>> raise_warn('MyWarn1', 'test mywarn', logger=logger)
    >>> raise_warn('MyWarn2', 'test mywarn', code=1, logger=logger)
    >>> raise_warn('MyWarn1', 'test mywarn')
    >>> raise_warn('MyWarn1', 'test mywarn', code=2)
    """
    
    exec('class {}(Warning): pass'.format(name))
    
    codestr = '' if not code else 'WarnCode: %s, '%code
    filename, lineno, line = get_caller_pos_info(stacklevel=3)
    prefix = 'DrmKtWarn' if 'logger' not in kwargs else 'LogDrmKtWarn'
    wmsg = '{} at {}, line: {}:\n  {}\n{}{}: {}'.format(
            prefix, filename, lineno, line, codestr, name, msg)
    
    def __dramkit_warn_fmt(message, category, filename, lineno, line):
        """临时改变warning输出格式"""
        return '{}'.format(message)
    
    if 'logger' not in kwargs:
        _formatwarning = warnings.formatwarning
        warnings.formatwarning = __dramkit_warn_fmt
        warnings.warn(wmsg, category=eval(name))
        warnings.formatwarning = _formatwarning
        return
    
    with warnings.catch_warnings(record=True) as warns:
        warnings.warn(wmsg, category=eval(name))
        for warn in warns:
            logger_show(wmsg, logger=kwargs['logger'], level='warn')
    
    # 要让外部能捕捉到警告同时又不想重复显示警告信息
    # 办法是临时修改warning.formatwarning
    if can_catch:
        _formatwarning = warnings.formatwarning
        def __shutwarnformat(message, category, filename, lineno, line=None):
            return ''
        warnings.formatwarning = __shutwarnformat
        warnings.warn(wmsg, category=eval(name))  # 外部捕捉到的是这里
        warnings.formatwarning = _formatwarning


def catch_warnings(logger=None, log_repeat=False):
    """
    作为装饰器捕获函数运行警告
    
    Parameters
    ----------
    logger : None, logging.Logger
        日志记录器，若为None，则会优先使用被调用函数参数中的logger
    
    Examples
    --------
    .. code-block:: python
        :linenos:

        from dramkit import simple_logger
        logger = simple_logger()
        
        @catch_warnings(logger)
        def test_warn():
            # print('test warn...')
            raise_warn('TestWarn', 'test warn')

        @catch_warnings(logger)
        def test_warn0():
            # print('test warn0...')
            raise_warn('TestWarn', 'test warn', logger=logger)
            
        @catch_warnings(logger, log_repeat=True)
        def test_warn01():
            # print('test warn0...')
            raise_warn('TestWarn', 'test warn', logger=logger)
            
        @catch_warnings()
        def test_warn1(logger=None):
            raise_warn('TestWarn1', 'test warn1')
            
        @catch_warnings(simple_logger(logname='test'))
        @capture_print()
        def test_warn2(logger=None):
            print('test_warn2...')
            
        @catch_warnings(False)
        def test_warn3(logger=None):
            print('test_warn3...')
            raise_warn('TestWarn3', 'test warn3')
            
        @catch_warnings()
        def test_warn4(logger=None):
            print('test_warn4...')
            warnings.warn('TestWarn4')

    >>> test_warn()
    >>> test_warn0()
    >>> test_warn01()
    >>> test_warn1(logger=simple_logger('./_test/catch_warnings_test.log'))
    >>> test_warn2(logger=simple_logger('./_test/catch_warnings_test.log'))    
    >>> test_warn3()
    >>> test_warn4()
    """
    def transfunc(func):
        @wraps(func)
        def catcher(*args, **kwargs):
            '''运行func并捕获警告信息'''
            logger_ = __chose_logger(logger, kwargs)
            with warnings.catch_warnings(record=True) as warns:
                res = func(*args, **kwargs)
                for warn in warns:
                    wmsg = str(warn.message)
                    if wmsg.startswith('DrmKtWarn at '):  # raise_warn不带logger的情况
                        logger_show(wmsg, logger=logger_, level='warn')
                    elif wmsg.startswith('LogDrmKtWarn at '):  # raise_warn带logger的情况
                        if log_repeat:
                            logger_show(wmsg, logger=logger_, level='warn')
                    else:  # 非raise_warn的情况
                        filename, lineno, line = warn.filename, warn.lineno, warn.line
                        if line is None and os.path.exists(filename):
                            line = read_nlines(filename, lineno)[-1]
                        line = '' if line is None else '\n  '+line.rstrip()
                        logmsg = 'Warn at {}, line: {}:{}\n{}: {}'.format(
                                 filename, lineno, line, warn.category.__name__, wmsg.rstrip())
                        logger_show(logmsg, logger=logger_, level='warn')
                return res
        return catcher
    return transfunc
    

def raise_error(name: str,
                msg: str,
                code: Union[int, str] = None,
                **kwargs):
    """抛出异常，name异常名称、msg异常信息、code异常代码、logger日志记录器
    
    Examples
    --------
    >>> from dramkit import simple_logger
    >>> logger = simple_logger('./_test/test_raise_error.log', 'w')    
    >>> raise_error('MyError1', 'test myerror', logger=logger)
    >>> raise_error('MyError2', 'test myerror', code=1, logger=logger)
    """
    
    def __get_chain(stacks):
        res = []
        k = -2
        while k >= -len(stacks):
            stack = stacks[k]
            filename = stack.filename.replace(os.sep, '/')
            if ('site-packages/spyder_kernels' not in filename) and \
               ('site-packages/IPython' not in filename):
                res.append(stack)
                k -= 1
            else:
                break
        return res[::-1]
    
    exec('class {}(Exception): pass'.format(name))
    if not 'logger' in kwargs:
        exec('raise {}("{}")'.format(name, msg))
    else:
        try:
            exec('raise {}("{}")'.format(name, '(LogDrmKtErr) '+msg))
        except:
            stacks = __get_chain(traceback.extract_stack())
            strs = traceback.format_list(stacks)
            emsg = traceback.format_exc().rstrip().split('\n')
            prefix = emsg[0]
            emsg = '\n'.join(emsg[1:])
            logmsg = prefix+'\n'+'\n'.join([x.rstrip() for x in strs]+[emsg])
            if not isnull(code):
                logmsg = 'ErrorCode: %s\n'%code + logmsg
            logger_show(logmsg, logger=kwargs['logger'],
                        level='err', err_exc_info=False)
            raise
        
        
class RaiseError(object):
    
    def __init__(self, logger=None):
        self.logger = logger
        
    def raise_error(self, name, msg, code=None):
        raise_error(name, msg, code=code, logger=self.logger)


def catch_error(logger=None, raise_error=True,
                show_params=False, log_repeat=False):
    """作为装饰器捕获函数运行错误
    
    Parameters
    ----------
    logger : None, logging.Logger
        日志记录器，若为None，则会优先使用被调用函数参数中的logger
    
    Examples
    --------
    .. code-block:: python
        :linenos:

        from dramkit import simple_logger
        logger = simple_logger()

        @catch_error(logger)
        def test_error():
            print('test_error...') 
            raise ValueError('test raise')
            
        @catch_error()
        def test_error1(logger=None):
            print('test_error1...')
            raise ValueError('test raise1')
            
        @catch_error(simple_logger(logname='test'))
        @capture_print()
        def test_error2(logger=None):
            print('test_error2...')
            
        @catch_error(False)
        def test_error3(logger=None):
            print('test_error3...')
            raise ValueError('test raise3')

    >>> test_error()
    >>> test_error1(logger=simple_logger('./_test/catch_error_test.log'))
    >>> test_error2(logger=simple_logger('./_test/catch_error_test.log'))    
    >>> test_error3()    
    """
    
    def __get_chain(stacks):
        res = []
        k = -2
        while k >= -len(stacks):
            stack = stacks[k]
            filename = stack.filename.replace(os.sep, '/')
            if ('site-packages/spyder_kernels' not in filename) and \
               ('site-packages/IPython' not in filename):
                res.append(stack)
                k -= 1
            else:
                break
        return res[::-1]
    
    def transfunc(func):
        @wraps(func)
        def catcher(*args, **kwargs):
            '''运行func并捕获错误信息'''
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if (not str(e).lstrip().startswith('(LogDrmKtErr) ')) or log_repeat:
                    emsg = traceback.format_exc().rstrip().split('\n')
                    prefix = emsg[0]
                    emsg = '\n'.join(emsg[1:])
                    logger_ = __chose_logger(logger, kwargs)
                    stacks = __get_chain(traceback.extract_stack())
                    strs = traceback.format_list(stacks)
                    emsg = prefix+'\n'+'\n'.join([x.rstrip() for x in strs]+[emsg])
                    err = 'func `%s` error info:\n%s'%(func.__name__, emsg)
                    if show_params:
                        err = err + '\nparams: %s, %s'%(args, kwargs)
                    logger_show(err, logger_, 'error', err_exc_info=False)
                if raise_error:
                    raise
                else:
                    return None
        return catcher
    return transfunc


def capture_print(logger=None, del_last_blank=True, ori_print=False):
    """作为装饰器捕获函数中的print内容
    
    Parameters
    ----------
    logger : None, logging.Logger
        日志记录器，若为None，则会优先使用被调用函数参数中的logger
    
    Examples
    --------
    .. code-block:: python
        :linenos:

        from dramkit import simple_logger
        logger = simple_logger()

        @capture_print(logger)
        def test_print():
            print('test_print...')
            
        @capture_print()
        def test_print1(logger=None):
            print('test_print1...')
            
        @capture_print(simple_logger(logname='test'))
        def test_print2(logger=None):
            print('test_print2...')
            
        @capture_print(False)
        def test_print3(logger=None):
            print('test_print3...')
            
        @capture_print()
        def test_print4(**kwargs):
            print('test_print4...')

    >>> test_print()
    test_print...
        [INFO: 2023-04-29 10:45:41,671]
    >>> test_print1(logger=simple_logger('./_test/capture_print_test.log'))
    >>> test_print2(logger=simple_logger('./_test/capture_print_test.log'))    
    >>> test_print3()
    >>> test_print4(logger=simple_logger('./_test/capture_print_test.log'))
    """
    def transfunc(func):
        @wraps(func)
        def capturer(*args, **kwargs):
            '''运行func并捕获print内容'''
            # 替换默认的标准输出流
            output = StringIO()
            sys.stdout = output
            result = func(*args, **kwargs)
            # 恢复标准输出流，捕获内容
            sys.stdout = sys.__stdout__
            strs = output.getvalue()
            if del_last_blank and len(strs) > 0:
                strs = strs[:-1] if strs[-1] in string.whitespace else strs
            # if del_last_blank:
            #     strs = strs.rstrip()
            if len(strs) > 0:
                if ori_print:
                    print(strs)
                else:
                    logger_ = __chose_logger(logger, kwargs)
                    logger_show(strs, logger_, 'info')
            return result
        return capturer
    return transfunc


def record_run_time(logger=None):
    '''
    作为装饰器记录函数进入、退出时间以及用时
    
    Examples
    --------
    .. code-block:: python
        :linenos:

        from dramkit import simple_logger
        logger = simple_logger()

        @record_run_time(logger)
        def wait():
            print('wait...')
            time.sleep(3)

        @record_run_time()
        def wait1(logger=None):
            print('wait...')
            time.sleep(3)
            
        @record_run_time(simple_logger(logname='test'))
        def wait2(logger=None):
            print('wait...')
            time.sleep(3)
            
        @record_run_time(False)
        def wait3(logger=None):
            print('wait...')
            time.sleep(3)

    >>> wait()
    enter func `wait` at: 2023-07-06 16:45:26.
        [INFO: 2023-07-06 16:45:26,042]
    wait...
    exit func `wait` at: 2023-07-06 16:45:29.
        [INFO: 2023-07-06 16:45:29,048]
    func `wait` run time: 3.006651s.
        [INFO: 2023-07-06 16:45:29,049]
    >>> wait1(logger=simple_logger('./_test/record_run_time_test.log'))
    >>> wait1(logger=simple_logger('./_test/record_run_time_test.log', screen_show=False))
    >>> wait2(logger=simple_logger('./_test/record_run_time_test.log'))    
    >>> wait3()

    See Also
    --------
    :func:`dramkit.gentools.log_used_time`
    '''
    def transfunc(func):
        @wraps(func)
        def timer(*args, **kwargs):
            '''运行func并记录用时'''
            logger_ = __chose_logger(logger, kwargs)
            t0 = time.time()
            logger_show('enter func `%s` at: %s.'%(func.__name__, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t0))),
                        logger_, 'info')
            result = func(*args, **kwargs)
            t = time.time()
            # logger_show('exit func `%s` at: %s.'%(func.__name__, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))),
            #             logger_, 'info')
            logger_show('func `%s` run time: %ss.'%(func.__name__, round(t-t0, 6)),
                        logger_, 'info')
            return result
        return timer
    return transfunc


def log_used_time(logger=None):
    '''
    作为装饰器记录函数运行用时
    
    Parameters
    ----------
    logger : None, logging.Logger
        日志记录器，若为None，则会优先使用被调用函数参数中的logger

    Examples
    --------
    .. code-block:: python
        :linenos:

        from dramkit import simple_logger
        logger = simple_logger()

        @log_used_time(logger)
        def wait():
            print('wait...')
            time.sleep(3)

        @log_used_time()
        def wait1(logger=None):
            print('wait...')
            time.sleep(3)
            
        @log_used_time(simple_logger(logname='test'))
        def wait2(logger=None):
            print('wait...')
            time.sleep(3)
            
        @log_used_time(False)
        def wait3(logger=None):
            print('wait...')
            time.sleep(3)

    >>> wait()
    wait...
    func `wait` run time: 3.0s.
        [INFO: 2023-04-20 13:39:37,292]
    >>> wait1(logger=simple_logger('./_test/log_used_time_test.log'))
    >>> wait2(logger=simple_logger('./_test/log_used_time_test.log'))    
    >>> wait3()

    See Also
    --------
    :func:`dramkit.gentools.print_used_time`

    References
    ----------
    - https://www.cnblogs.com/xiuyou/p/11283512.html
    - https://www.cnblogs.com/slysky/p/9777424.html
    - https://www.cnblogs.com/zhzhang/p/11375574.html
    - https://www.cnblogs.com/zhzhang/p/11375774.html
    - https://blog.csdn.net/weixin_33711647/article/details/92549215
    '''
    def transfunc(func):
        @wraps(func)
        def timer(*args, **kwargs):
            '''运行func并记录用时'''
            t0 = time.monotonic()
            result = func(*args, **kwargs)
            t = time.monotonic()
            logger_ = __chose_logger(logger, kwargs)
            logger_show('func `%s` run time: %ss.'%(func.__name__, round(t-t0, 6)),
                        logger_, 'info')
            return result
        return timer
    return transfunc


def print_used_time(func):
    '''
    作为装饰器打印函数运行用时
    
    Parameters
    ----------
    func : function
        需要记录运行用时的函数
    
    Examples
    --------
    .. code-block:: python
        :linenos:
            
        from dramkit import simple_logger

        @print_used_time
        def wait(x, **kwargs):
            print('wait...')
            time.sleep(x)

    >>> wait(3)
    wait...
    func `wait` run time: 3.0s.
    >>> wait(x=3, b=5, logger=simple_logger())
    wait...
    func `wait` run time: 3.0s.
        [INFO: 2023-04-20 13:22:32,643]

    See Also
    --------
    :func:`dramkit.gentools.log_used_time`

    References
    ----------
    - https://www.cnblogs.com/slysky/p/9777424.html
    - https://www.cnblogs.com/zhzhang/p/11375574.html
    '''
    @wraps(func)
    def timer(*args, **kwargs):
        '''运行func并print用时'''
        t0 = time.monotonic()
        result = func(*args, **kwargs)
        t = time.monotonic()
        if 'logger' in kwargs:
            logger_show('func `%s` run time: %ss.'%(func.__name__, round(t-t0, 6)), kwargs['logger'])
        else:
            print('func `%s` run time: %ss.'%(func.__name__, round(t-t0, 6)))
        return result
    return timer


def func_params_process_decorator(func_params, *args_p, **kwargs_p):
    '''
    | 作为装饰器，在调用函数之前对函数入参进行处理 
    | func_params接收参数顺序必须为func_params(*args_p, *args, **kwargs_p, **kwargs) 
    | 其中args_p, kwargs_p为func_params本身参数，args和kwargs为目标函数参数

    Examples
    --------
    >>> def params_process(a, *args, b=3, **kwargs):
    ...    args = list(args)
    ...    args[0] = args[0] + a
    ...    if 'z' in kwargs:
    ...        kwargs['z'] = kwargs['z'] + b
    ...    return args, kwargs
    ...
    ... @func_params_process_decorator(params_process, 2, b=4)
    ... def a(x, y, z=4):
    ...     return x+y+z
    >>> a(2, 3)
    11
    >>> a(2, 3, z=5)
    16
    '''
    def transfunc(func):
        @wraps(func)
        def processer(*args, **kwargs):
            '''函数结果处理'''
            args_, kwargs_ = func_params(
                             *args_p, *args, **kwargs_p, **kwargs)
            res = func(*args_, **kwargs_)
            return res
        return processer
    return transfunc


def func_res_process_decorator(func_res, *args_res, **kwargs_res):
    '''
    作为装饰器处理函数输出结果
    
    Examples
    --------
    >>> def res_process(res, k, b):
    ...    return res * k + b
    ...
    ... @func_res_process_decorator(res_process, 2, 5)
    ... def a(x, y):
    ...     return x+y
    >>> a(2, 3)
    15
    '''
    def transfunc(func):
        @wraps(func)
        def processer(*args, **kwargs):
            '''函数结果处理'''
            res = func(*args, **kwargs)
            res = func_res(res, *args_res, **kwargs_res)
            return res
        return processer
    return transfunc


def func_runtime_test(func, n=10000, return_all=False,
                      *args, **kwargs):
    '''函数性能（运行时间）测试，n设置测试运行测试'''
    if not return_all:
        tr = TimeRecoder()
        for _ in tqdm(range(n)):
        # for _ in range(n):
        #     pstr = '{}/{}, {}%'.format(_+1, n, round(100*(_+1)/n, 2))
        #     print('\r', pstr, end='', flush=True)
            res = func(*args, **kwargs)
        # print('')
        t = tr.useds()
        return t, res
    else:
        tr = TimeRecoder()
        res_all = []
        for _ in tqdm(range(n)):
        # for _ in range(n):
        #     pstr = '{}/{}, {}%'.format(_+1, n, round(100*(_+1)/n, 2))
        #     print('\r', pstr, end='', flush=True)
            res = func(*args, **kwargs)
            res_all.append(res)
        # print('')
        t = tr.useds()
        return t, res_all
    
    
def check_list_arg(arg, allow_none=False):
    '''检查arg，若其不是list或tuple或set，则转为列表'''
    if not allow_none and isnull(arg):
        raise ValueError('不支持`arg`为无效值！')
    if isnull(arg):
        return arg
    if not isinstance(arg, (list, tuple, set)):
        arg = [arg]
    return arg


def get_update_kwargs(key, arg, kwargs, arg_default=None,
                      func_update=None):
    '''
    取出并更新kwargs中key参数的值

    使用场景：当一个函数接受**kwargs参数，同时需要对kwargs里面的某个key的值进行更新并且
    提取出来单独传参

    Parameters
    ----------
    key : 'str'
        kwargs中待取出并更新的关键字
    arg : Any
        关键字key对应的新值
    kwargs : dict
        关键字参数对
    arg_default : key关键词对应参数默认值
    func_update : None, False, function
        自定义取出的key参数值更新函数: arg_new = func_update(arg, arg_old)

        - 若为False, 则不更新，直接取出原来key对应的参数值或默认值
        - 若为`replace`, 则直接替换更新
        - 若为None, 则 **默认** 更新方式为:

            * 若参数值arg为dict或list类型，则增量更新
            * 若参数值arg_old为list且arg不为list，则增量更新
            * 其它情况直接替换更新

    Returns
    -------
    arg_new :
        取出并更新之后的关键字key对应参数值
    kwargs :
        删除key之后的kwargs

    Examples
    --------
    >>> key, arg = 'a', 'aa'
    >>> kwargs = {'a': 'a', 'b': 'b'}
    >>> get_update_kwargs(key, arg, kwargs)
    ('aa', {'b': 'b'})
    >>> key, arg = 'a', {'a_': 'aa__'}
    >>> kwargs = {'a': {'a': 'aa'}, 'b': 'b'}
    >>> get_update_kwargs(key, arg, kwargs)
    ({'a': 'aa', 'a_': 'aa__'}, {'b': 'b'})
    >>> key, arg = 'a', ['aa', 'aa_']
    >>> kwargs = {'a': ['a'], 'b': 'b'}
    >>> get_update_kwargs(key, arg, kwargs)
    (['a', 'aa', 'aa_'], {'b': 'b'})
    >>> key, arg = 'a', ['aa', 'aa_']
    >>> kwargs = {'a': ['a'], 'b': 'b'}
    >>> get_update_kwargs(key, arg, kwargs, func_update='replace')
    (['aa', 'aa_'], {'b': 'b'})
    >>> key, arg = 'a', 'aa_'
    >>> kwargs = {'a': ['a'], 'b': 'b'}
    >>> get_update_kwargs(key, arg, kwargs)
    (['a', 'aa_'], {'b': 'b'})
    '''
    
    kwargs = kwargs.copy()
    
    def _default_update(arg, arg_old):
        if isinstance(arg, dict):
            assert isinstance(arg_old, dict) or isnull(arg_old)
            arg_new = {} if isnull(arg_old) else arg_old
            arg_new.update(arg)
        elif isinstance(arg, list):
            assert isinstance(arg_old, list) or isnull(arg_old)
            arg_new = [] if isnull(arg_old) else arg_old
            arg_new += arg
        elif isinstance(arg_old, list) and not isinstance(arg, list):
            arg_new = arg_old + [arg]
        else:
            arg_new = arg
        return arg_new

    # 取出原来的值
    if key in kwargs.keys():
        arg_old = kwargs[key]
        del kwargs[key]
    else:
        arg_old = arg_default

    # 不更新
    if func_update is False:
        return arg_old, kwargs

    # 更新
    if func_update is None:
        func_update = _default_update
    elif func_update == 'replace':
        func_update = lambda arg, arg_old: arg
    arg_new = func_update(arg, arg_old)
        
    return arg_new, kwargs


@beartype
def roulette_base(fitness: Union[list, tuple, dict, np.ndarray]):
    '''
    基本轮盘赌法
    
    TODO
    ----
    fitness有负数时的轮盘赌法
    
    Parameters
    ----------
    fitness : list
        所有备选对象的fitness值列表

        .. note::
            fitness的元素值应为正，且fitness值越大，被选中概率越大


    :returns: `int` - 返回被选中对象的索引号

    References
    ----------
    https://blog.csdn.net/armwangEric/article/details/50775206
    '''
    if isinstance(fitness, dict):
        sum_fits = sum(list(fitness.values()))
    else:
        sum_fits = sum(fitness)
        fitness = dict(enumerate(fitness))
    rand_point = uniform(0, sum_fits)
    accumulator = 0.0
    for idx, fitn in fitness.items():
        accumulator += fitn
        if rand_point <= accumulator:
            return idx


def roulette_stochastic_accept(fitness: Union[list, tuple, dict, np.ndarray]):
    '''
    轮盘赌法，随机接受法
    
    Parameters
    ----------
    fitness : list
        所有备选对象的fitness值列表

        .. note::
            fitness的元素值应为正，且fitness值越大，被选中概率越大


    :returns: `int` - 返回被选中对象的索引号

    References
    ----------
    https://blog.csdn.net/armwangEric/article/details/50775206
    '''
    if not isinstance(fitness, dict):
        fitness = dict(enumerate(fitness))
    n = len(fitness)
    max_fit = max(list(fitness.values()))
    keys = list(fitness.keys())
    while True:
        idx = randint(0, n-1)
        if random() <= fitness[keys[idx]] / max_fit:
            return keys[idx]


def roulette_count(fitness, n=10000, rand_func=None):
    '''
    轮盘赌法n次模拟，返回每个备选对象在n次模拟中被选中的次数

    Parameters
    ----------
    fitness : list, dict
        所有备选对象的fitness值列表或字典，格式参见Example
        
        .. note::
            fitness的元素值应为正，且fitness值越大，被选中概率越大
    n : int
        模拟次数
    rand_func : None, function
        | 指定轮盘赌法函数，如'roulette_base'(:func:`dramkit.gentools.roulette_base`)
        | 或'roulette_stochastic_accept'(:func:`dramkit.gentools.roulette_stochastic_accept`),
        | 默认用'roulette_stochastic_accept'
        

    :returns: `list, dict` - 返回每个对象在模拟n次中被选中的次数

    Examples
    --------
    >>> fitness = [1, 2, 3]
    >>> roulette_count(fitness, n=6000)
    [(0, 991), (1, 2022), (2, 2987)]
    >>> fitness = (1, 2, 3)
    >>> roulette_count(fitness, n=6000)
    [(0, 1003), (1, 1991), (2, 3006)]
    >>> fitness = [('a', 1), ('b', 2), ('c', 3)]
    >>> roulette_count(fitness, n=6000)
    [('a', 997), ('b', 1989), ('c', 3014)]
    >>> fitness = [['a', 1], ['b', 2], ['c', 3]]
    >>> roulette_count(fitness, n=6000)
    [('a', 1033), ('b', 1967), ('c', 3000)]
    >>> fitness = {'a': 1, 'b': 2, 'c': 3}
    >>> roulette_count(fitness, n=6000)
    {'a': 988, 'b': 1971, 'c': 3041}
    '''
    
    if rand_func is None:
        rand_func = roulette_stochastic_accept
    
    if isinstance(fitness, dict):
        keys, vals = list(fitness.keys()), list(fitness.values())
        randpicks = [rand_func(vals) for _ in range(n)]
        idx_picks = [(x, randpicks.count(x)) for x in range(len(vals))]
        return {keys[x[0]]: x[1] for x in idx_picks}

    elif (isinstance(fitness[0], list) or isinstance(fitness[0], tuple)):
        keys, vals = [], []
        for k, v in fitness:
            keys.append(k)
            vals.append(v)
        randpicks = [rand_func(vals) for _ in range(n)]
        idx_picks = [(x, randpicks.count(x)) for x in range(len(vals))]
        return [(keys[x[0]], x[1]) for x in idx_picks]

    elif (isinstance(fitness[0], int) or isinstance(fitness[0], float)):
        randpicks = [rand_func(fitness) for _ in range(n)]
        idx_picks = [(x, randpicks.count(x)) for x in range(len(fitness))]
        return idx_picks
    
    raise ValueError('未识别的fitness格式！')


def rand_sum(target_sum, n, lowests, highests, isint=True, n_dot=6):
    '''
    在指定最大最小值范围内随机选取若干个随机数，所选取数之和为定值

    Parameters
    ----------
    target_sum : int, float
        目标和
    n : int
        随机选取个数
    lowests : int, floot, list
        随机数下限值，若为list，则其第k个元素对应第k个随机数的下限
    highests : int, floot, list
        随机数上限值，若为list，则其第k关元素对应第k个随机数的上限
    isint : bool
        所选数是否强制为整数，若为False，则为实数
        
        .. note::
            若输入lowests或highests不是int，则isint为True无效
    n_dot : int
        动态上下界值与上下限比较时控制小数位数(为了避免python精度问题导致的报错)


    :returns: `list` - 随机选取的n个数，其和为target_sum

    Examples
    --------
    >>> rand_sum(100, 2, [20, 30], 100)
    [65, 35]
    >>> rand_sum(100, 2, 20, 100)
    [41, 59]
    >>> rand_sum(100, 2, [20, 10], [100, 90])
    [73, 27]
    '''

    if not (isinstance(lowests, int) or isinstance(lowests, float)): 
        if len(lowests) != n:
            raise ValueError('下限值列表(数组)lowests长度必须与n相等！')
    if  not (isinstance(highests, int) or isinstance(highests, float)):
        if len(highests) != n:
            raise ValueError('上限值列表(数组)highests长度必须与n相等！')

    # lowests、highests组织成list
    if isinstance(lowests, int) or isinstance(lowests, float):
        lowests = [lowests] * n
    if isinstance(highests, int) or isinstance(highests, float):
        highests = [highests] * n

    if any([isinstance(x, float) for x in lowests]) or any([isinstance(x, float) for x in highests]):
        isint = False

    LowHigh = list(zip(lowests, highests))

    def _dyLowHigh(tgt_sum, low_high, n_dot=6):
        '''
        动态计算下界和上界
        tgt_sum为目标和，low_high为上下界对组成的列表
        n_dot为小数保留位数(为了避免python精度问题导致的报错)
        '''
        restSumHigh = sum([x[1] for x in low_high[1:]])
        restSumLow = sum([x[0] for x in low_high[1:]])
        low = max(tgt_sum-restSumHigh, low_high[0][0])
        if round(low, n_dot) > low_high[0][1]:
            raise ValueError(
               '下界({})超过最大值上限({})！'.format(low, low_high[0][1]))
        high = min(tgt_sum-restSumLow, low_high[0][1])
        if round(high, n_dot) < low_high[0][0]:
            raise ValueError(
               '上界({})超过最小值下限({})！'.format(high, low_high[0][0]))
        return low, high

    S = 0
    adds = []
    low, high = _dyLowHigh(target_sum, LowHigh, n_dot=n_dot)
    while len(adds) < n-1:
        # 每次随机选择一个数
        if isint:
            randV = randint(low, high)
        else:
            randV = random() * (high-low) + low

        # 判断当前所选择的备选数是否符合条件，若符合则加入备选数，
        # 若不符合则删除所有备选数重头开始
        restSum = target_sum - (S + randV)
        restSumLow = sum([x[0] for x in LowHigh[len(adds)+1:]])
        restSumHigh = sum([x[1] for x in LowHigh[len(adds)+1:]])
        if restSumLow <= restSum <= restSumHigh:
            S += randV
            adds.append(randV)
            low, high = _dyLowHigh(target_sum-S, LowHigh[len(adds):],
                                  n_dot=n_dot)
        else:
            S = 0
            adds = []
            low, high = _dyLowHigh(target_sum, LowHigh, n_dot=n_dot)

    adds.append(target_sum-sum(adds)) # 最后一个备选数

    return adds


def rand_weight_sum(weight_sum, n, lowests, highests, weights=None, n_dot=6):
    '''
    在指定最大最小值范围内随机选取若干个随机数，所选取数之加权和为定值

    Parameters
    ----------
    weight_sum : float
        目标加权和
    n : int
        随机选取个数
    lowests : int, floot, list
        随机数下限值，若为list，则其第k个元素对应第k个随机数的下限
    highests : int, floot, list
        随机数上限值，若为list，则其第k关元素对应第k个随机数的上限
    weights : None, list
        权重列表
        
        .. note::
            lowests和highests与weights应一一对应
    n_dot : int
        动态上下界值与上下限比较时控制小数位数(为了避免python精度问题导致的报错)


    :returns: `list` - 随机选取的n个数，其以weights为权重的加权和为weight_sum

    Examples
    --------
    >>> rand_weight_sum(60, 2, [20, 30], 100)
    [21.41082008017613, 98.58917991982386]
    >>> rand_weight_sum(70, 2, 20, 100)
    [56.867261610484356, 83.13273838951565]
    >>> rand_weight_sum(80, 2, [20, 10], [100, 90])
    [80.32071140116187, 79.67928859883813]
    >>> rand_weight_sum(80, 2, [20, 10], [100, 90], [0.6, 0.4])
    [88.70409567475888, 66.94385648786168]
    >>> rand_weight_sum(180, 2, [20, 10], [100, 90], [3, 2])
    [23.080418085462018, 55.37937287180697]
    >>> rand_sum(1, 4, 0, 1)
    [0, 1, 0, 0]
    >>> print([round(x, 4) for x in rand_sum(1, 4, 0.0, 1.0)])
    [0.1896, 0.1913, 0.0797, 0.5394]
    '''

    if weights is not None and len(weights) != n:
        raise ValueError('权重列表W的长度必须等于n！')
    if not (isinstance(lowests, int) or isinstance(lowests, float)):
        if len(lowests) != n:
            raise ValueError('下限值列表(数组)lowests长度必须与n相等！')
    if not (isinstance(highests, int) or isinstance(highests, float)):
        if len(highests) != n:
            raise ValueError('上限值列表(数组)highests长度必须与n相等！')

    # weights和lowests、highests组织成list
    if weights is None:
        weights = [1/n] * n
    if isinstance(lowests, int) or isinstance(lowests, float):
        lowests = [lowests] * n
    if isinstance(highests, int) or isinstance(highests, float):
        highests = [highests] * n

    WLowHigh = list(zip(weights, lowests, highests))

    def _dyLowHigh(wt_sum, w_low_high, n_dot=6):
        '''
        动态计算下界和上界
        wt_sum为目标加权和，w_low_high为权重和上下界三元组组成的列表
        n_dot为小数保留位数(为了避免python精度问题导致的报错)
        '''
        restSumHigh = sum([x[2]*x[0] for x in w_low_high[1:]])
        restSumLow = sum([x[1]*x[0] for x in w_low_high[1:]])
        low = max((wt_sum-restSumHigh) / w_low_high[0][0], w_low_high[0][1])
        if round(low, n_dot) > w_low_high[0][2]:
            raise ValueError(
               '下界({})超过最大值上限({})！'.format(low, w_low_high[0][2]))
        high = min((wt_sum-restSumLow) / w_low_high[0][0], w_low_high[0][2])
        if round(high, n_dot) < w_low_high[0][1]:
            raise ValueError(
               '上界({})超过最小值下限({})！'.format(high, w_low_high[0][1]))
        return low, high

    S = 0
    adds = []
    low, high = _dyLowHigh(weight_sum, WLowHigh, n_dot=n_dot)
    while len(adds) < n-1:
        # 每次随机选择一个数
        randV = random() * (high-low) + low

        # 判断当前所选择的备选数是否符合条件，若符合则加入备选数，
        # 若不符合则删除所有备选数重头开始
        restSum = weight_sum - (S + randV * weights[len(adds)])
        restSumLow = sum([x[1]*x[0] for x in WLowHigh[len(adds)+1:]])
        restSumHigh = sum([x[2]*x[0] for x in WLowHigh[len(adds)+1:]])
        if restSumLow <= restSum <= restSumHigh:
            S += randV * weights[len(adds)]
            adds.append(randV)
            low, high = _dyLowHigh(weight_sum-S, WLowHigh[len(adds):],
                                  n_dot=n_dot)
        else:
            S = 0
            adds = []
            low, high = _dyLowHigh(weight_sum, WLowHigh, n_dot=n_dot)

    aw = zip(adds, weights[:-1])
    adds.append((weight_sum-sum([a*w for a, w in aw])) / weights[-1])

    return adds


def replace_repeat_iter(series, val, val0, gap=None, keep_last=False):
    '''
    替换序列中重复出现的值
    
    | series (`pd.Series`) 中若步长为gap的范围内出现多个val值，则只保留第一条记录，
      后面的替换为val0
    | 若gap为None，则将连续出现的val值只保留第一个，其余替换为val0(这里连续出现val是指
      不出现除了val和val0之外的其他值)
    | 若keep_last为True，则连续的保留最后一个
    
    返回结果为替换之后的series (`pd.Series`)

    Examples
    --------
    >>> data = pd.DataFrame([0, 1, 1, 0, -1, -1, 2, -1, 1, 0, 1, 1, 1, 0, 0,
    ...                      -1, -1, 0, 0, 1], columns=['test'])
    >>> data['test_rep'] = replace_repeat_iter(data['test'], 1, 0, gap=None)
    >>> data
        test  test_rep
    0      0         0
    1      1         1
    2      1         0
    3      0         0
    4     -1        -1
    5     -1        -1
    6      2         2
    7     -1        -1
    8      1         1
    9      0         0
    10     1         0
    11     1         0
    12     1         0
    13     0         0
    14     0         0
    15    -1        -1
    16    -1        -1
    17     0         0
    18     0         0
    19     1         1
    >>> series = pd.Series([-1, 1, -1, 0, 1, 0, 1, 1, -1])
    >>> replace_repeat_iter(series, 1, 0, gap=5)
    0   -1
    1    1
    2   -1
    3    0
    4    1
    5    0
    6    0
    7    0
    8   -1
    '''
    if not keep_last:
        return _replace_repeat_iter(series, val, val0, gap=gap)
    else:
        series_ = series[::-1]
        series_ = _replace_repeat_iter(series_, val, val0, gap=gap)
        return series_[::-1]


@beartype
def _get_out1(series: SeriesType,
              df: pd.DataFrame,
              cols: Union[str, List[str]]
              ) -> Union[pd.Series, np.ndarray, list, tuple]:
    _cols = check_list_arg(cols)
    if isinstance(series, pd.Series):
        df.index = series.index
        res = [df[c] for c in _cols]
    elif isinstance(series, np.ndarray):
        res = [df[c].values for c in _cols]
    else:
        res = [df[c].tolist() for c in _cols]
    if isinstance(cols, str):
        return res[0]
    return tuple(res)


@beartype
def _get_out2(series: SeriesType,
              *ss
              ) -> Union[pd.Series, np.ndarray, list, tuple]:
    if isinstance(series, pd.Series):
        res = [pd.Series(s, index=series.index) for s in ss]
    elif isinstance(series, np.ndarray):
        res = [np.array(s) for s in ss]
    else:
        res = [list(s) for s in ss]
    if len(ss) == 1:
        return res[0]
    return tuple(res)
    

@beartype
def replace_repeat(series: SeriesType,
                   val: Any,
                   val0: Any,
                   gap: int = None):
    res = np.array(series)
    k, n = 0, len(res)
    while k < n:
        if res[k] == val:
            k1 = k + 1
            imax = n if isna(gap) else k+gap
            while k1 < imax and res[k1] in [val, val0]:
                if res[k1] == val:
                    res[k1] = val0
                k1 += 1
            k =  k1
        else:
            k += 1
    return _get_out2(series, res)


def _replace_repeat_iter(series, val, val0, gap=None):
    '''
    TODO
    ----
    改为不在df里面算（df.loc可能会比较慢？）
    '''

    col = series.name
    df = pd.DataFrame({col: series})

    if gap is not None and (gap > df.shape[0] or gap < 1):
        raise ValueError('gap取值范围必须为1到df.shape[0]之间！')
    gap = None if gap == 1 else gap

    # 当series.index存在重复值时为避免报错，因此先重置index最后再还原
    ori_index = df.index
    df.index = range(0, df.shape[0])

    k = 0
    while k < df.shape[0]:
        if df.loc[k, col] == val:
            k1 = k + 1

            if gap is None:
                while k1 < df.shape[0] and \
                                    df.loc[k1, col] in [val, val0]:
                    if df.loc[k1, col] == val:
                        df.loc[k1, col] = val0
                    k1 += 1
            else:
                while k1 < min(k+gap, df.shape[0]) and \
                                    df.loc[k1, col] in [val, val0]:
                    if df.loc[k1, col] == val:
                        df.loc[k1, col] = val0
                    k1 += 1
            k =  k1

        else:
            k += 1

    df.index = ori_index

    return df[col]
    
    
def replace_repeat_pd(series, val, val0, keep_last=False):
    '''
    | 替换序列中重复出现的值, 仅保留第一个
    | 
    | 函数功能，参数和意义同 :func:`dramkit.gentools.replace_repeat_iter`
    | 区别在于计算时在pandas.DataFrame里面进行而不是采用迭代方式，同时取消了gap
      参数(即连续出现的val值只保留第一个)
    '''
    if not keep_last:
        return _replace_repeat_pd(series, val, val0)
    else:
        series_ = series[::-1]
        series_ = _replace_repeat_pd(series_, val, val0)
        return series_[::-1]


def _replace_repeat_pd(series, val, val0):
    col = series.name
    df = pd.DataFrame({col: series})
    # 为了避免计算过程中临时产生的列名与原始列名混淆，对列重新命名
    col_ori = col
    col = 'series'
    df.columns = [col]

    # 当series.index存在重复值时为避免报错，因此先重置index最后再还原
    ori_index = df.index
    df.index = range(0, df.shape[0])

    df['gap1'] = df[col].apply(lambda x: x not in [val, val0]).astype(int)
    df['is_val'] = df[col].apply(lambda x: x == val).astype(int)
    df['val_or_gap'] = df['gap1'] + df['is_val']
    df['pre_gap'] = df[df['val_or_gap'] == 1]['gap1'].shift(1)
    if pd.__version__ < '2.1.0':
        df['pre_gap'] = df['pre_gap'].fillna(method='ffill')
    else:
        df['pre_gap'] = df['pre_gap'].ffill()
    k = 0
    while k < df.shape[0] and df.loc[k, 'is_val'] != 1:
        k += 1
    if k < df.shape[0]:
        df.loc[k, 'pre_gap'] = 1
    df['pre_gap'] = df['pre_gap'].fillna(0).astype(int)
    df['keep1'] = (df['is_val'] + df['pre_gap']).map({0: 0, 1: 0, 2: 1})
    df['to_rplc'] = (df['keep1'] + df['is_val']).map({2: 0, 1: 1, 0: 0})
    df[col] = df[[col, 'to_rplc']].apply(lambda x:
                            val0 if x['to_rplc'] == 1 else x[col], axis=1)

    df.rename(columns={col: col_ori}, inplace=True)
    df.index = ori_index

    return df[col_ori]
    
    
def replace_repeat_func_iter(series, func_val, func_val0,
                             gap=None, keep_last=False):
    '''
    | 替换序列中重复出现的值，功能与 :func:`dramkit.gentools.replace_repeat_iter`
      类似，只不过把val和val0的值由直接指定换成了由指定函数生成

    | ``func_val`` 函数用于判断连续条件，其返回值只能是True或False，
    | ``func_val0`` 函数用于生成替换的新值。
    | 即series中若步长为gap的范围内出现多个满足func_val函数为True的值， 
      则只保留第一条记录，后面的替换为函数func_val0的值。
    | 若gap为None，则将连续出现的满足func_val函数为True的值只保留第一个，其余替换为函数
      func_val0的值(这里连续出现是指不出现除了满足func_val为True和等于func_val0函数值
      之外的其他值)
    
    返回结果为替换之后的series (`pd.Series`)

    Examples
    --------
    >>> data = pd.DataFrame({'y': [0, 1, 1, 0, -1, -1, 2, -1, 1, 0, 1,
    ...                            1, 1, 0, 0, -1, -1, 0, 0, 1]})
    >>> data['y_rep'] = replace_repeat_func_iter(
    ...                 data['y'], lambda x: x < 1, lambda x: 3, gap=None)
    >>> data
        y  y_rep
    0   0      0
    1   1      1
    2   1      1
    3   0      0
    4  -1      3
    5  -1      3
    6   2      2
    7  -1     -1
    8   1      1
    9   0      0
    10  1      1
    11  1      1
    12  1      1
    13  0      0
    14  0      3
    15 -1      3
    16 -1      3
    17  0      3
    18  0      3
    19  1      1
    '''
    if not keep_last:
        return _replace_repeat_func_iter(series, func_val, func_val0, gap=gap)
    else:
        series_ = series[::-1]
        series_ = _replace_repeat_func_iter(series_, func_val, func_val0, gap=gap)
        return series_[::-1]


def _replace_repeat_func_iter(series, func_val, func_val0, gap=None):
    col = series.name
    df = pd.DataFrame({col: series})

    if gap is not None and (gap > df.shape[0] or gap < 1):
        raise ValueError('gap取值范围必须为1到df.shape[0]之间！')
    gap = None if gap == 1 else gap

    # 当series.index存在重复值时为避免报错，因此先重置index最后再还原
    ori_index = df.index
    df.index = range(0, df.shape[0])

    k = 0
    while k < df.shape[0]:
        if func_val(df.loc[k, col]):
            k1 = k + 1

            if gap is None:
                while k1 < df.shape[0] and \
                                    (func_val(df.loc[k1, col]) \
                                     or df.loc[k1, col] == \
                                        func_val0(df.loc[k1, col])):
                    if func_val(df.loc[k1, col]):
                        df.loc[k1, col] = func_val0(df.loc[k1, col])
                    k1 += 1
            else:
                while k1 < min(k+gap, df.shape[0]) and \
                                (func_val(df.loc[k1, col]) \
                                 or df.loc[k1, col] == \
                                    func_val0(df.loc[k1, col])):
                    if func_val(df.loc[k1, col]):
                        df.loc[k1, col] = func_val0(df.loc[k1, col])
                    k1 += 1
            k =  k1

        else:
            k += 1

    df.index = ori_index

    return df[col]
    
    
def replace_repeat_func_pd(series, func_val, func_val0, keep_last=False):
    '''
    替换序列中重复出现的值, 仅保留第一个
    
    | 函数功能，参数和意义同 :func:`dramkit.gentools.replace_repeat_func_iter`
    | 区别在于计算时在pandas.DataFrame里面进行而不是采用迭代方式
    | 同时取消了gap参数(即连续出现的满足func_val为True的值只保留第一个)
    '''
    if not keep_last:
        return _replace_repeat_func_pd(series, func_val, func_val0)
    else:
        series_ = series[::-1]
        series_ = _replace_repeat_func_pd(series_, func_val, func_val0)
        return series_[::-1]


def _replace_repeat_func_pd(series, func_val, func_val0):
    col = series.name
    df = pd.DataFrame({col: series})
    # 为了避免计算过程中临时产生的列名与原始列名混淆，对列重新命名
    col_ori = col
    col = 'series'
    df.columns = [col]

    # 当series.index存在重复值时为避免报错，因此先重置index最后再还原
    ori_index = df.index
    df.index = range(0, df.shape[0])

    df['gap1'] = df[col].apply(lambda x:
                               not func_val(x) and x != func_val0(x)).astype(int)
    df['is_val'] = df[col].apply(lambda x: func_val(x)).astype(int)
    df['val_or_gap'] = df['gap1'] + df['is_val']
    df['pre_gap'] = df[df['val_or_gap'] == 1]['gap1'].shift(1)
    if pd.__version__ < '2.1.0':
        df['pre_gap'] = df['pre_gap'].fillna(method='ffill')
    else:
        df['pre_gap'] = df['pre_gap'].ffill()
    k = 0
    while k < df.shape[0] and df.loc[k, 'is_val'] != 1:
        k += 1
    if k < df.shape[0]:
        df.loc[k, 'pre_gap'] = 1
    df['pre_gap'] = df['pre_gap'].fillna(0).astype(int)
    df['keep1'] = (df['is_val'] + df['pre_gap']).map({0: 0, 1: 0, 2: 1})
    df['to_rplc'] = (df['keep1'] + df['is_val']).map({2: 0, 1: 1, 0: 0})
    df[col] = df[[col, 'to_rplc']].apply(
              lambda x: func_val0(x[col]) if x['to_rplc'] == 1 else x[col],
              axis=1)

    df.rename(columns={col: col_ori}, inplace=True)
    df.index = ori_index

    return df[col_ori]


def con_count(series, func_cond, via_pd=True):
    '''
    计算series(pd.Series)中连续满足func_cond函数指定的条件的记录数

    Parameters
    ----------
    series : pd.Series
        目标序列
    func_cond : function
        指定条件的函数，func_cond(x)返回结果只能为True或False
    via_pd : bool
        若via_pd为False，则计算时使用循环迭代，否则在pandas.DataFrame里面进行计算


    :returns: `pd.Series` - 返回连续计数结果

    Examples
    --------
    >>> df = pd.DataFrame([0, 0, 1, 1, 0, 0, 1, 1, 1], columns=['series'])
    >>> func_cond = lambda x: True if x == 1 else False
    >>> df['count1'] = con_count(df['series'], func_cond, True)
    >>> df
       series  count1
    0       0       0
    1       0       0
    2       1       1
    3       1       2
    4       0       0
    5       0       0
    6       1       1
    7       1       2
    8       1       3
    >>> df['count0'] = con_count(df['series'], lambda x: x != 1, False)
    >>> df
       series  count1  count0
    0       0       0       1
    1       0       0       2
    2       1       1       0
    3       1       2       0
    4       0       0       1
    5       0       0       2
    6       1       1       0
    7       1       2       0
    8       1       3       0
    '''

    col = 'series'
    series.name = col
    df = pd.DataFrame(series)

    # 当series.index存在重复值时为避免报错，因此先重置index最后再还原
    ori_index = df.index
    df.index = range(0, df.shape[0])

    if via_pd:
        df['Fok'] = df[col].apply(lambda x: func_cond(x)).astype(int)
        df['count'] = df['Fok'].cumsum()
        df['tmp'] = df[df['Fok'] == 0]['count']
        if pd.__version__ < '2.1.0':
            df['tmp'] = df['tmp'].fillna(method='ffill')
        else:
            df['tmp'] = df['tmp'].ffill()
        df['tmp'] = df['tmp'].fillna(0)
        df['count'] = (df['count'] - df['tmp']).astype(int)

        df.index = ori_index

        return df['count']

    else:
        df['count'] = 0
        k = 0
        while k < df.shape[0]:
            if func_cond(df.loc[k, col]):
                count = 1
                df.loc[k, 'count'] = count
                k1 = k + 1
                while k1 < df.shape[0] and func_cond(df.loc[k1, col]):
                    count += 1
                    df.loc[k1, 'count'] = count
                    k1 += 1
                k = k1
            else:
                k += 1

        df.index = ori_index

        return df['count']


def con_count_ignore(series, func_cond, via_pd=True, func_ignore=None):
    '''
    在 :func:`dramkit.gentools.con_count` 的基础上增加连续性判断条件:

        当series中的值满足func_ignore函数值为True时，不影响连续性判断(func_ignore
        默认为 ``lambda x: isnull(x)``)
    '''
    if func_ignore is None:
        func_ignore = lambda x: isnull(x)
    df = pd.DataFrame({'v': series})
    df['ignore'] = df['v'].apply(lambda x: func_ignore(x)).astype(int)
    df['count'] = con_count(df[df['ignore'] == 0]['v'], func_cond, via_pd=via_pd)
    df['count'] = df['count'].fillna(0)
    df['count'] = df['count'].astype(int)
    return df['count']


def get_preval_func_cond(data, col_val, col_cond, func_cond):
    '''
    | 获取上一个满足指定条件的行中col_val列的值，条件为：
    | 该行中col_cond列的值x满足func_cond(x)为True (func_cond(x)返回结果只能为True或False)
    | 返回结果为 `pd.Series`

    Examples
    --------
    >>> data = pd.DataFrame({'x1': [0, 1, 1, 0, -1, -1, 2, -1, 1, 0, 1, 1, 1,
    ...                             0, 0, -1, -1, 0, 0, 1],
    ...                      'x2': [0, 1, 1, 0, -1, -1, 1, -1, 1, 0, 1, 1, 1,
    ...                             0, 0, -1, -1, 0, 0, 1]})
    >>> data['x1_pre'] = get_preval_func_cond(data, 'x1', 'x2', lambda x: x != 1)
    >>> data
        x1  x2  x1_pre
    0    0   0     NaN
    1    1   1     0.0
    2    1   1     0.0
    3    0   0     0.0
    4   -1  -1     0.0
    5   -1  -1    -1.0
    6    2   1    -1.0
    7   -1  -1    -1.0
    8    1   1    -1.0
    9    0   0    -1.0
    10   1   1     0.0
    11   1   1     0.0
    12   1   1     0.0
    13   0   0     0.0
    14   0   0     0.0
    15  -1  -1     0.0
    16  -1  -1    -1.0
    17   0   0    -1.0
    18   0   0     0.0
    19   1   1     0.0
    '''

    df = data[[col_val, col_cond]].copy()
    # 为了避免计算过程中临时产生的列名与原始列名混淆，对列重新命名
    col_val, col_cond = ['col_val', 'col_cond']
    df.columns = [col_val, col_cond]

    df['Fok'] = df[col_cond].apply(lambda x: func_cond(x)).astype(int)
    df['val_pre'] = df[df['Fok'] == 1][col_val]
    if pd.__version__ < '2.1.0':
        df['val_pre'] = df['val_pre'].shift(1).fillna(method='ffill')
    else:
        df['val_pre'] = df['val_pre'].shift(1).ffill()

    return df['val_pre']


def gap_count(series, func_cond, via_pd=True):
    '''
    计算series (`pd.Series`)中当前行距离上一个满足 ``func_cond`` 函数指定条件记录的行数
    
    func_cond为指定条件的函数，func_cond(x)返回结果只能为True或False，
    若via_pd为False，则使用循环迭代，若via_pd为True，则在pandas.DataFrme内计算
    返回结果为 `pd.Series`

    Examples
    --------
    >>> df = pd.DataFrame([0, 1, 1, 0, 0, 1, 1, 1], columns=['series'])
    >>> func_cond = lambda x: True if x == 1 else False
    >>> df['gap1'] = gap_count(df['series'], func_cond, True)
    >>> df
       series  gap1
    0       0     0
    1       1     0
    2       1     1
    3       0     1
    4       0     2
    5       1     3
    6       1     1
    7       1     1
    >>> df['gap0'] = gap_count(df['series'], lambda x: x != 1, False)
    >>> df
       series  gap1  gap0
    0       0     0     0
    1       1     0     1
    2       1     1     2
    3       0     1     3
    4       0     2     1
    5       1     3     1
    6       1     1     2
    7       1     1     3
    '''

    col = 'series'
    series.name = col
    df = pd.DataFrame(series)

    # 当series.index存在重复值时为避免报错，因此先重置index最后再还原
    ori_index = df.index
    df.index = range(0, df.shape[0])

    if via_pd:
        df['idx'] = range(0, df.shape[0])
        df['idx_pre'] = get_preval_func_cond(df, 'idx', col, func_cond)
        df['gap'] = (df['idx'] - df['idx_pre']).fillna(0).astype(int)

        df.index = ori_index

        return df['gap']

    else:
        df['count'] = con_count(series, lambda x: not func_cond(x), via_pd=via_pd)

        df['gap'] = df['count']
        k0 = 0
        while k0 < df.shape[0] and not func_cond(df.loc[k0, col]):
            df.loc[k0, 'gap'] = 0
            k0 += 1

        for k1 in range(k0+1, df.shape[0]):
            if func_cond(df.loc[k1, col]):
                df.loc[k1, 'gap'] = df.loc[k1-1, 'count'] + 1

        df.index = ori_index

        return df['gap']


def count_between_gap(data, col_gap, col_count, func_gap, func_count,
                      count_now_gap=False, count_now=True, via_pd=True):
    '''
    计算data (`pandas.DataFrame`)中当前行与上一个满足 ``func_gap`` 函数为True的行之间，
    满足 ``func_count`` 函数为True的记录数

    | 函数func_gap作用于 ``col_gap`` 列，func_count作用于 ``col_count`` 列，
      两者返回值均为True或False
    | ``count_now_gap`` 设置满足func_gap的行是否参与计数，若为False，
      则该行计数为0，若为True，则该行按照上一次计数的最后一次计数处理
    
    .. todo::
        增加count_now_gap的处理方式：
        
        - 该行计数为0
        - 该行按上一次计数的最后一次计数处理
        - 该行按下一次计数的第一次计数处理

    ``count_now`` 设置当当前行满足func_count时，从当前行开始对其计数还是从下一行开始对其计数
    
    .. note::
        注：当前行若满足同时满足func_gap和func_count，对其计数的行不会为下一行
        (即要么不计数，要么在当前行对其计数)

    若via_pd为True，则调用 :func:`count_between_gap_pd` 实现，否则用 :func:`count_between_gap_iter`

    返回结果为 `pd.Series`

    Examples
    --------
    >>> data = pd.DataFrame({'to_gap': [0, 1, 1, 0, -1, -1, 2, -1, 1, 0, -1, 1,
    ...                                 1, 0, 0, -1, -1, 0, 0, 1],
    ...                      'to_count': [0, 1, 1, 0, -1, -1, 1, -1, 1, 0, 1,
    ...                                   1, 1, 0, 0, -1, -1, 0, 0, 1]})
    >>> data['gap_count'] = count_between_gap(data, 'to_gap', 'to_count',
    ...                                       lambda x: x == -1, lambda x: x == 1,
    ...                                       count_now_gap=False, count_now=False)
    >>> data
            to_gap  to_count  gap_count
    0        0         0          0
    1        1         1          0
    2        1         1          0
    3        0         0          0
    4       -1        -1          0
    5       -1        -1          0
    6        2         1          0
    7       -1        -1          0
    8        1         1          0
    9        0         0          1
    10      -1         1          0
    11       1         1          0
    12       1         1          1
    13       0         0          2
    14       0         0          2
    15      -1        -1          0
    16      -1        -1          0
    17       0         0          0
    18       0         0          0
    19       1         1          0
    >>> data = pd.DataFrame({'to_gap': [0, 1, 1, 0, -1, -1, 2, -1, 1, 0, -1, 1,
                                        1, 0, 0, -1, -1, 0, 0, 1, -1, -1],
                             'to_count': [0, 1, 1, 0, -1, -1, 1, -1, 1, 0, 1,
                                          1, 1, 0, 0, -1, 1, 0, 1, 1, 1, 1]})
    >>> data['gap_count'] = count_between_gap(data, 'to_gap', 'to_count',
                                              lambda x: x == -1, lambda x: x == 1,
                                              count_now_gap=False, count_now=True)
    >>> data
            to_gap  to_count  gap_count
    0        0         0          0
    1        1         1          0
    2        1         1          0
    3        0         0          0
    4       -1        -1          0
    5       -1        -1          0
    6        2         1          1
    7       -1        -1          0
    8        1         1          1
    9        0         0          1
    10      -1         1          0
    11       1         1          1
    12       1         1          2
    13       0         0          2
    14       0         0          2
    15      -1        -1          0
    16      -1         1          0
    17       0         0          0
    18       0         1          1
    19       1         1          2
    20      -1         1          0
    21      -1         1          0
    >>> data = pd.DataFrame({'to_gap': [0, 1, 1, 0, -1, -1, 2, -1, 1, 0, -1, 1,
                                        1, 0, 0, -1, -1, 0, 0, 1, -1, -1],
                             'to_count': [0, -1, -1, 0, -1, -1, 1, -1, 1, 0, 1, 1,
                                          1, 0, 0, -1, -1, 0, -1, 1, 1, 1]})
    >>> data['gap_count'] = count_between_gap(data, 'to_gap', 'to_count',
                                              lambda x: x == -1, lambda x: x == 1,
                                              count_now_gap=True, count_now=False)
    >>> data
            to_gap  to_count  gap_count
    0        0         0          0
    1        1        -1          0
    2        1        -1          0
    3        0         0          0
    4       -1        -1          0
    5       -1        -1          0
    6        2         1          0
    7       -1        -1          1
    8        1         1          0
    9        0         0          1
    10      -1         1          1
    11       1         1          0
    12       1         1          1
    13       0         0          2
    14       0         0          2
    15      -1        -1          2
    16      -1        -1          0
    17       0         0          0
    18       0        -1          0
    19       1         1          0
    20      -1         1          1
    21      -1         1          0
    >>> data = pd.DataFrame({'to_gap': [0, 1, 1, 0, -1, -1, 2, -1, 1, 0, -1, 1,
                                        1, 0, 0, -1, -1, 0, 0, 1, -1, -1],
                             'to_count': [0, -1, -1, 0, -1, -1, 1, -1, 1, 0, 1, 1,
                                          1, 0, 0, -1, -1, 0, -1, 1, 1, 1]})
    >>> data['gap_count'] = count_between_gap(data, 'to_gap', 'to_count',
                                              lambda x: x == -1, lambda x: x == 1,
                                              count_now_gap=True, count_now=True)
    >>> data
            to_gap  to_count  gap_count
    0        0         0          0
    1        1        -1          0
    2        1        -1          0
    3        0         0          0
    4       -1        -1          0
    5       -1        -1          0
    6        2         1          1
    7       -1        -1          1
    8        1         1          1
    9        0         0          1
    10      -1         1          2
    11       1         1          1
    12       1         1          2
    13       0         0          2
    14       0         0          2
    15      -1        -1          2
    16      -1        -1          0
    17       0         0          0
    18       0        -1          0
    19       1         1          1
    20      -1         1          2
    21      -1         1          1
    '''

    if via_pd:
        return count_between_gap_pd(data, col_gap, col_count, func_gap,
                                    func_count, count_now_gap=count_now_gap,
                                    count_now=count_now)
    else:
        return count_between_gap_iter(data, col_gap, col_count, func_gap,
                                      func_count, count_now_gap=count_now_gap,
                                      count_now=count_now)


def count_between_gap_pd(data, col_gap, col_count, func_gap, func_count,
                         count_now_gap=True, count_now=True):
    '''参数和功能说明见 :func:`dramkit.gentools.count_between_gap` 函数'''

    df = data[[col_gap, col_count]].copy()
    # 为了避免计算过程中临时产生的列名与原始列名混淆，对列重新命名
    col_gap, col_count = ['col_gap', 'col_count']
    df.columns = [col_gap, col_count]

    df['gap0'] = df[col_gap].apply(lambda x: not func_gap(x)).astype(int)
    df['count1'] = df[col_count].apply(lambda x: func_count(x)).astype(int)
    df['gap_count'] = df[df['gap0'] == 1]['count1'].cumsum()
    df['gap_cut'] = df['gap0'].diff().shift(-1)
    df['gap_cut'] = df['gap_cut'].apply(lambda x: 1 if x == -1 else np.nan)
    df['tmp'] = (df['gap_count'] * df['gap_cut']).shift(1)
    if pd.__version__ < '2.1.0':
        df['tmp'] = df['tmp'].fillna(method='ffill')
    else:
        df['tmp'] = df['tmp'].ffill()
    df['gap_count'] = df['gap_count'] - df['tmp']

    if count_now_gap:
        df['pre_gap0'] = df['gap0'].shift(1)
        df['tmp'] = df['gap_count'].shift()
        df['tmp'] = df[df['gap0'] == 0]['tmp']

        df['gap_count1'] = df['gap_count'].fillna(0)
        df['gap_count2'] = df['tmp'].fillna(0) + df['count1'] * (1-df['gap0'])
        df['gap_count'] = df['gap_count1'] + df['gap_count2']

    if not count_now:
        df['gap_count'] = df['gap_count'].shift(1)
        if not count_now_gap:
            df['gap_count'] = df['gap0'] * df['gap_count']
        else:
            df['gap_count'] = df['pre_gap0'] * df['gap_count']

    df['gap_count'] = df['gap_count'].fillna(0).astype(int)

    return df['gap_count']


def count_between_gap_iter(data, col_gap, col_count, func_gap, func_count,
                           count_now_gap=True, count_now=True):
    '''参数和功能说明见 :func:`dramkit.gentools.count_between_gap` 函数'''

    df = data[[col_gap, col_count]].copy()
    # 为了避免计算过程中临时产生的列名与原始列名混淆，对列重新命名
    col_gap, col_count = ['col_gap', 'col_count']
    df.columns = [col_gap, col_count]

    # 当data.index存在重复值时为避免报错，因此先重置index最后再还原
    ori_index = df.index
    df.index = range(0, df.shape[0])

    df['gap_count'] = 0

    k = 0
    while k < df.shape[0]:
        if func_gap(df.loc[k, col_gap]):
            k += 1
            gap_count = 0
            while k < df.shape[0] and \
                                  not func_gap(df.loc[k, col_gap]):
                if func_count(df.loc[k, col_count]):
                    gap_count += 1
                df.loc[k, 'gap_count'] = gap_count
                k += 1
        else:
            k += 1

    if count_now_gap:
        k = 1
        while k < df.shape[0]:
            if func_gap(df.loc[k, col_gap]):
                if not func_gap(df.loc[k-1, col_gap]):
                    if func_count(df.loc[k, col_count]):
                        df.loc[k, 'gap_count'] = \
                                        df.loc[k-1, 'gap_count'] + 1
                        k += 1
                    else:
                        df.loc[k, 'gap_count'] = \
                                            df.loc[k-1, 'gap_count']
                        k += 1
                else:
                    if func_count(df.loc[k, col_count]):
                        df.loc[k, 'gap_count'] = 1
                        k += 1
                    else:
                        k += 1
            else:
                k += 1

    if not count_now:
        df['gap_count_pre'] = df['gap_count'].copy()
        if not count_now_gap:
            for k in range(1, df.shape[0]):
                if func_gap(df.loc[k, col_gap]):
                    df.loc[k, 'gap_count'] = 0
                else:
                    df.loc[k, 'gap_count'] = \
                                        df.loc[k-1, 'gap_count_pre']
        else:
            for k in range(1, df.shape[0]):
                if func_gap(df.loc[k-1, col_gap]):
                    df.loc[k, 'gap_count'] = 0
                else:
                    df.loc[k, 'gap_count'] = \
                                        df.loc[k-1, 'gap_count_pre']
        df.drop('gap_count_pre', axis=1, inplace=True)

    k0 = 0
    while k0 < df.shape[0] and not func_gap(df.loc[k0, col_gap]):
        df.loc[k0, 'gap_count'] = 0
        k0 += 1
    df.loc[k0, 'gap_count'] = 0

    df.index = ori_index

    return df['gap_count']


def val_gap_cond(data, col_val, col_cond, func_cond, func_val,
                 to_cal_col=None, func_to_cal=None, val_nan=np.nan,
                 contain_1st=False):
    '''
    计算data (`pandas.DataFrame`)中从上一个 ``col_cond`` 列满足 ``func_cond`` 函数的行
    到当前行, ``col_val`` 列记录的 ``func_val`` 函数值

    | func_cond作用于col_cond列，func_cond(x)返回True或False，x为单个值
    | func_val函数作用于col_val列，func_val(x)返回单个值，x为np.array或pd.Series或列表等
    | func_to_cal作用于to_cal_col列，只有当前行func_to_cal值为True时才进行func_val计算，
      否则返回结果中当前行值设置为val_nan
    | contain_1st设置func_val函数计算时是否将上一个满足func_cond的行也纳入计算

    .. todo::
        参考 :func:`dramkit.gentools.count_between_gap` 的设置:

        - 设置col_cond列满足func_cond函数的行，其参与func_val函数的前一次计算还是下一次计算还是不参与计算

    Examples
    --------
    >>> data = pd.DataFrame({'val': [1, 2, 5, 3, 1, 7 ,9],
    ...                      'sig': [1, 1, -1, 1, 1, -1, 1]})
    >>> data['val_pre1'] = val_gap_cond(data, 'val', 'sig',
    ...                    lambda x: x == -1, lambda x: max(x))
    >>> data
       val  sig  val_pre1
    0    1    1       NaN
    1    2    1       NaN
    2    5   -1       NaN
    3    3    1       3.0
    4    1    1       3.0
    5    7   -1       7.0
    6    9    1       9.0
    '''

    if to_cal_col is None and func_to_cal is None:
        df = data[[col_val, col_cond]].copy()
        # 为了避免计算过程中临时产生的列名与原始列名混淆，对列重新命名
        col_val, col_cond = ['col_val', 'col_cond']
        df.columns = [col_val, col_cond]
    elif to_cal_col is not None and func_to_cal is not None:
        df = data[[col_val, col_cond, to_cal_col]].copy()
        # 为了避免计算过程中临时产生的列名与原始列名混淆，对列重新命名
        col_val, col_cond, to_cal_col = ['col_val', 'col_cond',
                                                               'to_cal_col']
        df.columns = [col_val, col_cond, to_cal_col]

    df['idx'] = range(0, df.shape[0])
    df['pre_idx'] = get_preval_func_cond(df, 'idx', col_cond, func_cond)

    if to_cal_col is None and func_to_cal is None:
        if not contain_1st:
            df['gap_val'] = df[['pre_idx', 'idx', col_val]].apply(lambda x:
               func_val(df[col_val].iloc[int(x['pre_idx']+1): int(x['idx']+1)]) \
               if not isnull(x['pre_idx']) else val_nan, axis=1)
        else:
            df['gap_val'] = df[['pre_idx', 'idx', col_val]].apply(lambda x:
               func_val(df[col_val].iloc[int(x['pre_idx']): int(x['idx']+1)]) \
               if not isnull(x['pre_idx']) else val_nan, axis=1)
    elif to_cal_col is not None and func_to_cal is not None:
        if not contain_1st:
            df['gap_val'] = df[['pre_idx', 'idx', col_val,
                                                to_cal_col]].apply(lambda x:
              func_val(df[col_val].iloc[int(x['pre_idx']+1): int(x['idx']+1)]) \
              if not isnull(x['pre_idx']) and func_to_cal(x[to_cal_col]) else \
              val_nan, axis=1)
        else:
            df['gap_val'] = df[['pre_idx', 'idx', col_val,
                                                to_cal_col]].apply(lambda x:
              func_val(df[col_val].iloc[int(x['pre_idx']): int(x['idx']+1)]) \
              if not isnull(x['pre_idx']) and func_to_cal(x[to_cal_col]) else \
              val_nan, axis=1)

    return df['gap_val']


def filter_by_func_prenext(l, func_prenext):
    '''
    对 ``l`` (`list`)进行过滤，过滤后返回的 ``lnew`` (`list`)任意前后相邻两个元素满足:

        func_prenext(lnew[i], lnew[i+1]) = True

    过滤过程为：将 ``l`` 的第一个元素作为起点，找到其后第一个满足 ``func_prenext`` 函数
    值为True的元素，再以该元素为起点往后寻找...

    Examples
    --------
    >>> l = [1, 2, 3, 4, 1, 1, 2, 3, 6]
    >>> func_prenext = lambda x, y: (y-x) >= 2
    >>> filter_by_func_prenext(l, func_prenext)
    [1, 3, 6]
    >>> l = [1, 2, 3, 4, 1, 5, 1, 2, 3, 6]
    >>> filter_by_func_prenext(l, func_prenext)
    [1, 3, 5]
    >>> filter_by_func_prenext(l, lambda x, y: y == x+1)
    [1, 2, 3, 4]
    >>> l = [(1, 2), (2, 3), (4, 1), (5, 0)]
    >>> func_prenext = lambda x, y: abs(y[-1]-x[-1]) == 1
    >>> filter_by_func_prenext(l, func_prenext)
    [(1, 2), (2, 3)]
    '''

    if len(l) == 0:
        return l

    lnew = [l[0]]
    idx_pre, idx_post = 0, 1
    while idx_post < len(l):
        vpre = l[idx_pre]
        idx_post = idx_pre + 1

        while idx_post < len(l):
            vpost = l[idx_post]

            if not func_prenext(vpre, vpost):
                idx_post += 1
            else:
                lnew.append(vpost)
                idx_pre = idx_post
                break

    return lnew


def filter_by_func_prenext_series(series, func_prenext,
                                  func_ignore=None, val_nan=np.nan):
    '''
    对series (`pandas.Series`)调用 ``filter_by_func_prenext`` 函数进行过滤，
    其中满足 ``func_ignore`` 函数为True的值不参与过滤，func_ignore函数默认为：
    ``lambda x: isnull(x)``

    series中 **被过滤的值** 在返回结果中用 ``val_nan`` 替换, **不参与过滤** 的值保持不变
    
    See Also
    --------
    :func:`dramkit.gentools.filter_by_func_prenext`

    Examples
    --------
    >>> series = pd.Series([1, 2, 3, 4, 1, 1, 2, 3, 6])
    >>> func_prenext = lambda x, y: (y-x) >= 2
    >>> filter_by_func_prenext_series(series, func_prenext)
    0    1.0
    1    NaN
    2    3.0
    3    NaN
    4    NaN
    5    NaN
    6    NaN
    7    NaN
    8    6.0
    >>> series = pd.Series([1, 2, 0, 3, 0, 4, 0, 1, 0, 0, 1, 2, 3, 6],
    ...                    index=range(14, 0, -1))
    >>> filter_by_func_prenext_series(series, func_prenext, lambda x: x == 0)
    14    1.0
    13    NaN
    12    0.0
    11    3.0
    10    0.0
    9     NaN
    8     0.0
    7     NaN
    6     0.0
    5     0.0
    4     NaN
    3     NaN
    2     NaN
    1     6.0
    '''
    
    if func_ignore is None:
        func_ignore = lambda x: isnull(x)

    l = [[k, series.iloc[k]] for k in range(0, len(series)) \
                                             if not func_ignore(series.iloc[k])]
    lnew = filter_by_func_prenext(l, lambda x, y: func_prenext(x[1], y[1]))

    i_l = [k for k, v in l]
    i_lnew = [k for k, v in lnew]
    idxs_ignore = [_ for _ in i_l if _ not in i_lnew]

    seriesNew = series.copy()
    for k in idxs_ignore:
        seriesNew.iloc[k] = val_nan

    return seriesNew


def df_na2value(df, value=None):
    '''
    | df中nan值替换为value
    | https://blog.csdn.net/Shone1214/article/details/125968784
    '''
    if pd.__version__ < '1.3.0':
        df = df.where(df.notna(), value)
    else:
        df = df.fillna(np.nan)
        df = df.replace({np.nan: value})
    return df


def copy_df_structure(df):
    '''复制df的结构到一个空的dataframe'''
    return df.drop(df.index)


def get_tmp_new(exists, tmp_new, ext='_'):
    '''以tmp_new为基础生成一个不在exists里面的值'''
    assert isinstance(exists, Iterable)
    assert isinstance(ext, (str, Callable))
    if isinstance(ext, str) and isinstance(tmp_new, str):
        while tmp_new in exists:
            tmp_new += ext
        return tmp_new
    while tmp_new in exists:
        tmp_new = ext(tmp_new)
    return tmp_new
    

def get_tmp_col(df, tmp_col_name):
    '''以tmp_col_name为基础生成一个不在df的列名中的列'''
    assert isinstance(tmp_col_name, str)
    return get_tmp_new(df.columns, tmp_col_name, ext='_')
    # while tmp_col_name in df.columns:
    #     tmp_col_name += '_'
    # return tmp_col_name


def merge_df(df_left, df_right, same_keep='left', **kwargs):
    '''
    在 ``pd.merge`` 上改进，相同列名时自动去除重复的

    Parameters
    ----------
    df_left : pandas.DataFrame
        待merge左表
    df_right : pandas.DataFrame
        待merge右表
    same_keep : str
        可选'left', 'right'，设置相同列保留左边df还是右边df
    **kwargs :
        pd.merge接受的其他参数


    :returns: `pandas.DataFrame` - 返回merge之后的数据表
    '''
    same_cols = [x for x in df_left.columns if x in df_right.columns]
    if len(same_cols) > 0:
        if 'on' in kwargs:
            if isinstance(kwargs['on'], list):
                same_cols = [x for x in same_cols if x not in kwargs['on']]
            elif isinstance(kwargs['on'], str):
                same_cols = [x for x in same_cols if x != kwargs['on']]
            else:
                raise ValueError('on参数只接受list或str！')
        if same_keep == 'left':
            df_right = df_right.drop(same_cols, axis=1)
        elif same_keep == 'right':
            df_left = df_left.drop(same_cols, axis=1)
        else:
            raise ValueError('same_keep参数只接受`left`或`right`！')
    return pd.merge(df_left, df_right, **kwargs)


def merge_dfs(dfs: Union[List[pd.DataFrame],
                         Tuple[pd.DataFrame]],
              **kw_updf):
    res = dfs[0]
    for k in range(1, len(dfs)):
        res = update_df(res, dfs[k], **kw_updf)
    return res
    
    
def update_df(df_old, df_new, idcols=None,
              del_dup_cols=None, rep_keep='new',
              sort_cols=None, ascendings=True,
              method='merge', logger=None):
    '''
    | 合并df_new到df_old
    | 注意：df_old和df_new不应该设置index
    | 注意：用merge处理当数据量大时占空间很大，method应设置为`concat`
    
    TODO
    ----
    增加对各列的类型进行指定的参数设置
    
    Examples
    --------
    >>> df_old = pd.DataFrame({'id1': [1, 2, 3, 4, 5],
    ...                        'id2': [2, 3, 4, 5, 6],
    ...                        'col1': ['a', 'b', 'c', 'd', 'e'],
    ...                        'col2': [2, 4, 6, 8, 10]})
    >>> df_new = pd.DataFrame({'id1': [3, 4, 5, 6, 7],
    ...                        'id2': [4, 5, 6, 7, 8],
    ...                        'col1': ['c', 'ddd', np.nan, 'f', 'g'],
    ...                        'col3': [6, 8, 10, 12, 14]})
    ... idcols = ['id1', 'id2']
    ... rep_keep = 'new'
    ... del_dup_cols = None#['id1', 'id2']
    >>> a = update_df(df_old, df_new,
    ...               idcols=idcols,
    ...               del_dup_cols=del_dup_cols,
    ...               rep_keep=rep_keep,
    ...               method='merge')
    >>> b = update_df(df_old, df_new,
    ...               idcols=idcols,
    ...               del_dup_cols=del_dup_cols,
    ...               rep_keep=rep_keep,
    ...               method='concat')
    '''
    assert rep_keep in ['new', 'old']
    assert method in ['merge', 'concat']
    if isnull(df_old) and isnull(df_new):
        logger_show('`df_old`和`df_new`均为无效值，返回None。', logger, 'warn')
        return None
    if isnull(df_old):
        df_old = copy_df_structure(df_new)
    if isnull(df_new):
        df_new = copy_df_structure(df_old)
    if any([not isnull(x) for x in df_old.index.names]):
        logger_show('`df_old`已存在的索引将被忽略！', logger, 'warn')
    if any([not isnull(x) for x in df_new.index.names]):
        logger_show('`df_new`已存在的索引将被忽略！', logger, 'warn')
    if not df_old.index.names == df_new.index.names:
        logger_show('`df_old`和`df_new`索引名称不一致！', logger, 'warn')
    df_old, df_new = df_old.copy(), df_new.copy()
    if isnull(idcols):
        res = pd.concat((df_old, df_new), axis=0)
    elif df_old.shape[0] < 1:
        res = df_new
    elif df_new.shape[0] < 1:
        res = df_old
    else:
        if method == 'merge':
            same_keep = 'left' if rep_keep == 'old' else 'right'
            both = merge_df(df_old, df_new, same_keep=same_keep,
                            how='inner', on=idcols)
            old = merge_df(df_old, df_new, same_keep='left',
                           how='left', on=idcols)
            new = merge_df(df_old, df_new, same_keep='right',
                           how='right', on=idcols)
            no_both = pd.concat((old, new), axis=0)
            no_both = no_both.drop_duplicates(subset=idcols,
                                              keep=False)
            res = pd.concat((no_both, both), axis=0)
        else:
            idcols = check_list_arg(idcols, allow_none=False)
            assert (df_old[idcols].dtypes != df_new[idcols].dtypes).sum() == 0
            both = [x for x in df_old.columns if x in df_new.columns]
            old = idcols + [x for x in df_old.columns if x not in df_new.columns]
            new = idcols + [x for x in df_new.columns if x not in df_old.columns]
            both = pd.concat((df_old[both], df_new[both]), axis=0)
            keep_ = 'last' if rep_keep == 'new' else 'first'
            both = both.drop_duplicates(subset=idcols, keep=keep_)
            res = pd.concat((both.set_index(idcols),
                             df_old[old].set_index(idcols),
                             df_new[new].set_index(idcols)),
                            axis=1).reset_index()
    if isnull(del_dup_cols):
        del_dup_cols = idcols
    del_dup_cols = check_list_arg(del_dup_cols, allow_none=True)
    if not isnull(del_dup_cols):
        keep_ = 'last' if rep_keep == 'new' else 'first'
        res = res.drop_duplicates(subset=del_dup_cols, keep=keep_)
    if isnull(sort_cols):
        sort_cols = idcols
    sort_cols = check_list_arg(sort_cols, allow_none=True)
    if not isnull(sort_cols):
        res = res.sort_values(sort_cols, ascending=ascendings)
    return res.reset_index(drop=True)


def dfs_concat_axis1(dfs_list, idcols=None,
                     ascending=True):
    '''多个df列表横向拼接'''
    if isnull(idcols):
        res = pd.concat(dfs_list, axis=1)
        res = res.sort_index(ascending=ascending)
    else:
        res = pd.concat([x.set_index(idcols) for x in dfs_list],
                        axis=1)
        res = res.reset_index()
        res = res.sort_values(idcols, ascending=ascending)
    return res


def cut_df_by_con_val(df, by_col, func_eq=None):
    '''
    根据 `by_col` 列的值，将 `df (pandas.DataFrame)` 切分为多个子集列表，返回 `list`
    
    切分依据：``func_eq`` 函数作用于 ``by_col`` 列，函数值连续相等的记录被划分到一个子集中

    Examples
    --------
    >>> df = pd.DataFrame({'val': range(0,10),
    ...                    'by_col': ['a']*3+['b']*2+['c']*1+['a']*3+['d']*1})
    >>> df.index = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q']
    >>> cut_df_by_con_val(df, 'by_col')
    [   val by_col
     z    0      a
     y    1      a
     x    2      a,
        val by_col
     w    3      b
     v    4      b,
        val by_col
     u    5      c,
        val by_col
     t    6      a
     s    7      a
     r    8      a,
        val by_col
     q    9      d]
    '''

    if isnull(func_eq):
        func_eq = lambda x: x
    df = df.copy()
    df['val_func_eq'] = df[by_col].apply(func_eq)
    by_col = 'val_func_eq'

    sub_dfs= []
    k = 0
    while k < df.shape[0]:
        k1 = k + 1
        while k1 < df.shape[0] and df[by_col].iloc[k1] == df[by_col].iloc[k]:
            k1 += 1
        sub_dfs.append(df.iloc[k:k1, :].drop(by_col, axis=1))
        k = k1

    return sub_dfs


def get_con_start_end(series, func_con):
    '''
    找出series (`pandas.Series`)中值连续满足 ``func_con`` 函数值为True的分段起止位置，
    返回起止位置对列表

    Examples
    --------
    >>> series = pd.Series([0, 1, 1, 0, 1, 1, 0, -1, -1, 0, 0, -1, 1, 1, 1, 1, 0, -1])
    >>> start_ends = get_con_start_end(series, lambda x: x == -1)
    >>> start_ends
    [[7, 8], [11, 11], [17, 17]]
    >>> start_ends = get_con_start_end(series, lambda x: x == 1)
    >>> start_ends
    [[1, 2], [4, 5], [12, 15]]
    '''

    start_ends = []
    # df['start'] = 0
    # df['end'] = 0
    start = 0
    N = len(series)
    while start < N:
        if func_con(series.iloc[start]):
            end = start
            while end < N and func_con(series.iloc[end]):
                end += 1
            start_ends.append([start, end-1])
            # df.loc[df.index[start], 'start'] = 1
            # df.loc[df.index[end-1], 'end'] = 1
            start = end + 1
        else:
            start += 1

    return start_ends


def cut_range_to_subs(n, gap):
    '''
    将 ``range(0, n)`` 切分成连续相接的子集:
    ``[range(0, gap), range(gap, 2*gap), ...]``
    '''
    n_ = n // gap
    mod = n % gap
    if mod != 0:
        return [(k*gap, (k+1)*gap) for k in range(0, n_)] + [(gap * n_, n)]
    else:
        return [(k*gap, (k+1)*gap) for k in range(0, n_)]


def cut_to_subs(l, gap):
    '''将列表分段，gap指定每段的个数'''
    idxs = cut_range_to_subs(len(l), gap)
    return [l[idx[0]: idx[1]] for idx in idxs]


def cut_to_n_subs(l: list, n: int, n_list: list = None):
    """将列表划分成n个子列表"""
    if n_list is not None:
        assert len(n_list) == n and sum(n_list) == len(l)
    else:
        num_per_sub = len(l) // n
        n_list = [num_per_sub] * n
        if len(l) % n != 0:
            n_list[-1] += len(l) % n
    idx_cumsum = np.cumsum([0] + n_list)
    return [l[idx_cumsum[k]: idx_cumsum[k+1]] for k in range(len(n_list))]


def check_l_allin_l0(l, l0):
    '''
    判断 ``l (list)`` 中的值是否都是 ``l0 (list)`` 中的元素, 返回True或False

    Examples
    --------
    >>> l = [1, 2, 3, -1, 0]
    >>> l0 = [0, 1, -1]
    >>> check_l_allin_l0(l, l0)
    False
    >>> l = [1, 1, 0, -1, -1, 0, 0]
    >>> l0 = [0, 1, -1]
    >>> check_l_in_l0(l, l0)
    True
    '''
    l_ = set(l)
    l0_ = set(l0)
    return len(l_-l0_) == 0


def check_exist_data(df, x_list, cols=None):
    '''
    依据指定的 ``cols`` 列检查 ``df (pandas.DataFrame)`` 中是否已经存在 ``x_list (list)`` 中的记录，
    返回list，每个元素值为True或False

    Examples
    --------
    >>> df = pd.DataFrame([['1', 2, 3.1, ], ['3', 4, 5.1], ['5', 6, 7.1]],
    ...                   columns=['a', 'b', 'c'])
    >>> x_list, cols = [[3, 4], ['3', 4]], ['a', 'b']
    >>> check_exist_data(df, x_list, cols=cols)
    [False, True]
    >>> check_exist_data(df, [['1', 3.1], ['3', 5.1]], ['a', 'c'])
    [True, True]
    '''

    if not isnull(cols):
        df_ = df.reindex(columns=cols)
    else:
        df_ = df.copy()
    data = df_.to_dict('split')['data']
    return [x in data for x in x_list]


def isnull(x):
    '''判断x是否为无效值(None, nan, x != x)，若是无效值，返回True，否则返回False'''
    if x is None:
        return True
    if x is np.nan:
        return True
    try:
        if x != x:
            return True
    except:
        try:
            if np.isnan(x):
                return True
            elif np.isnat(x):
                return True
        except:
            try:
                if pd.isnull(x):
                    return True
            except:
                pass
    return False


def isna(*args, **kwargs):
    return isnull(*args, **kwargs)


def x_div_y(x, y, v_x0=None, v_y0=0, v_xy0=1):
    '''
    x除以y

    - v_xy0为当x和y同时为0时的返回值
    - v_y0为当y等于0时的返回值
    - v_x0为当x等于0时的返回值
    '''
    if x == 0 and y == 0:
        return v_xy0
    if x != 0 and y == 0:
        return v_y0
    if x == 0 and y != 0:
        return 0 if v_x0 is None else v_x0
    return x / y


def power(a, b, return_real=True):
    '''计算a的b次方，return_real设置是否只返回实属部分'''
    c = a ** b
    if isnull(c):
        c = complex(a) ** complex(b)
    if return_real:
        c = c.real
    return c


def log(x, bottom=None):
    '''计算对数, bottom指定底'''
    assert isinstance(bottom, (int, float))
    if isnull(bottom):
        return np.log(x)
    return (np.log(x)) / (np.log(bottom)) # h换底公式


def cal_pct(v0, v1, vv00=1, vv10=-1):
    '''
    计算从v0到v1的百分比变化

    - vv00为当v0的值为0且v1为正时的返回值，v1为负时取负号
    - vv10为当v1的值为0且v0为正时的返回值，v0为负时取负号
    
    TODO
    ----
    正负无穷大处理
    '''
    if isnull(v0) or isnull(v1):
        return np.nan
    if v0 == 0:
        if v1 == 0:
            return 0
        elif v1 > 0:
            return vv00
        elif v1 < 0:
            return -vv00
    elif v1 == 0:
        if v0 > 0:
            return vv10
        elif v0 < 0:
            return -vv10
    elif v0 > 0:
        return v1 / v0 - 1
    elif v0 < 0:
        return -(v1 / v0 - 1)
    # elif v0 > 0 and v1 > 0:
    #     return v1 / v0 - 1
    # elif v0 < 0 and v1 < 0:
    #     return -(v1 / v0 - 1)
    # elif v0 > 0 and v1 < 0:
    #     return v1 / v0 - 1
    # elif v0 < 0 and v1 > 0:
    #     return -(v1 / v0 - 1)
    
    
def pct_change(series, lag=1):
    '''
    计算series百分比变化
    
    TODO
    ----
    分子分母为0或正负无穷大处理
    '''
    df = pd.DataFrame({'x': series})
    df['x_'] = df['x'].shift(lag)
    df['dif'] = df['x'] - df['x_']
    df['res'] = df['dif'] / df['x_'].abs()
    return df['res']


def s1divs2(series1, series2, vs20=np.nan):
    '''两个序列相比'''
    df = pd.DataFrame({'s1': series1, 's2': series2})
    df['res'] = df['s1'] / df['s2']
    df['res'] = df[['res', 's2']].apply(lambda x: x['res'] if x['s2'] != 0 else vs20, axis=1)    
    return df['res']


def min_com_multer(l):
    '''求一列数 `l (list)` 的最小公倍数，支持负数和浮点数'''
    l_max = max(l)
    mcm = l_max
    while any([mcm % x != 0 for x in l]):
        mcm += l_max
    return mcm


def max_com_divisor(l):
    '''
    求一列数 `l (list)` 的最大公约数，只支持正整数

    .. note::
        只支持正整数
    '''

    def _isint(x):
        '''判断x是否为整数'''
        tmp = str(x).split('.')
        if len(tmp) == 1 or all([x == '0' for x in tmp[1]]):
            return True
        return False

    if any([x < 1 or not _isint(x) for x in l]):
        raise ValueError('只支持正整数！')

    l_min = min(l)
    mcd = l_min
    while any([x % mcd != 0 for x in l]):
        mcd -= 1

    return mcd


def mcd2_tad(a, b):
    '''
    辗转相除法求a和b的最大公约数，a、b为正数
    
    .. note::
        - a, b应为正数
        - a, b为小数时由于精度问题会不正确
    '''
    if a < b:
        a, b = b, a # a存放较大值，b存放较小值
    if a % b == 0:
        return b
    else:
        return mcd2_tad(b, a % b)


def max_com_divisor_tad(l):
    '''
    用辗转相除法求一列数 `l (list)` 的最大公约数, `l` 元素均为正数

    .. note::
        - l元素均为正数
        - l元素为小数时由于精度问题会不正确

    References
    ----------
    https://blog.csdn.net/weixin_45069761/article/details/107954905
    '''
    
    # g = l[0]
    # for i in range(1, len(l)):
    #     g = mcd2_tad(g, l[i])
    # return g

    return reduce(lambda x, y: mcd2_tad(x, y), l)


def _pd_pivot_table(df, **kwargs):
    '''
    pandas中pivot_table函数测试
    
    Examples
    --------
    >>> df = pd.DataFrame(
    ...         {'类别': ['水果', '水果', '水果', '蔬菜', '蔬菜',
    ...                  '肉类', '肉类'],
    ...          '产地': ['美国', '中国', '中国', '中国',
    ...                  '新西兰', '新西兰', '美国'],
    ...          '名称': ['苹果', '梨', '草莓', '番茄', '黄瓜',
    ...                  '羊肉', '牛肉'],
    ...          '数量': [5, 5, 9, 3, 2, 10, 8],
    ...          '价格': [5, 5, 10, 3, 3, 13, 20]}
    ...         )
    >>> df1 = _pd_pivot_table(df,
    ...                       index=['产地', '类别'],
    ...                       # columns=['名称'],
    ...                       values=['数量', '价格'],
    ...                       # aggfunc='sum',
    ...                       aggfunc={'数量': 'sum', '价格': 'mean'},
    ...                       )
    
    References
    ----------
    - https://blog.csdn.net/bqw18744018044/article/details/80015840
    '''
    return df.pivot_table(**kwargs)


def _pd_crosstab(*args, **kwargs):
    '''
    pandas中crosstab函数测试
    
    Examples
    --------
    >>> df = pd.DataFrame(
    ...         {'类别': ['水果', '水果', '水果', '蔬菜', '蔬菜',
    ...                  '肉类', '肉类'],
    ...          '产地': ['美国', '中国', '中国', '中国',
    ...                  '新西兰', '新西兰', '美国'],
    ...          '名称': ['苹果', '梨', '草莓', '番茄', '黄瓜',
    ...                  '羊肉', '牛肉'],
    ...          '数量': [5, 5, 9, 3, 2, 10, 8],
    ...          '价格': [5, 5, 10, 3, 3, 13, 20]}
    ...         )
    >>> df1 = _pd_crosstab(index=df['类别'], columns=df['产地'], margins=True)
    >>> df2 = _pd_crosstab(index=df['产地'], columns=df['类别'],
    ...                    values=df['价格'], aggfunc='mean')
    
    References
    ----------
    - https://blog.csdn.net/bqw18744018044/article/details/80015840
    '''
    return pd.crosstab(*args, **kwargs)


def df_rows2cols(df, col_name, col_val_name,
                 fill_value=None):
    '''
    把df中col_value_name列数据按col_name列分组，通过unstack拆分为多列数据，新列名为col_name列中的值
    
    TODO
    ----
    有nan时的检查和处理
    
    Examples
    --------
    >>> df0 = pd.DataFrame(
    ...         [['Saliy', 'midterm', 'class1', 'A'],
    ...         ['Saliy', 'midterm', 'class3', 'B'],
    ...         ['Saliy', 'final', 'class1', 'C'],
    ...         ['Saliy', 'final', 'class3', 'C'],
    ...         ['Jeff', 'midterm', 'class2', 'D'],
    ...         ['Jeff', 'midterm', 'class4', 'A'],
    ...         ['Jeff', 'final', 'class2', 'E'],
    ...         ['Jeff', 'final', 'class4', 'C'],
    ...         ['Roger', 'midterm', 'class2', 'C'],
    ...         ['Roger', 'midterm', 'class5', 'B'],
    ...         ['Roger', 'final', 'class2', 'A'],
    ...         ['Roger', 'final', 'class5', 'A'],
    ...         ['Karen', 'midterm', 'class3', 'C'],
    ...         ['Karen', 'midterm', 'class4', 'A'],
    ...         ['Karen', 'final', 'class3', 'C'],
    ...         ['Karen', 'final', 'class4', 'A'],
    ...         ['Brain', 'midterm', 'class1', 'B'],
    ...         ['Brain', 'midterm', 'class5', 'A'],
    ...         ['Brain', 'final', 'class1', 'B'],
    ...         ['Brain', 'final', 'class5', 'C']],
    ...         columns=['name', 'test', 'class', 'grade'])
    >>> col_name, col_val_name = 'class', 'grade'
    >>> df1 = df_rows2cols(df0, col_name, col_val_name)
    >>> df2 = df_rows2cols(df0, col_name, col_val_name,
                           fill_value='None')
    '''
    idx_cols = [x for x in df.columns if not x in [col_name, col_val_name]]
    df = df.set_index(idx_cols+[col_name])
    df = df.unstack(fill_value=fill_value)
    df = df.reset_index()
    df.columns = idx_cols + [x[1] for x in df.columns[len(idx_cols):]]
    return df


def df_cols2rows(df, cols, col_name, col_val_name,
                 dropna=True):
    '''
    把df中指定的cols列数据通过stack堆积为行数据，新列名为col_name
    
    TODO
    ----
    有nan时的检查和处理
    
    Examples
    --------
    >>> na = [np.nan]
    >>> df3 = pd.DataFrame({'name': ['Saliy', 'Saliy', 'Jeff', 'Jeff',
    ...                              'Roger', 'Roger', 'Karen', 'Karen',
    ...                              'Brain', 'Brain'],
    ...                     'test': ['midterm', 'final'] * 5,
    ...                     'class1': ['A', 'C'] + na*6 + ['B', 'B'],
    ...                     'class2': na*2 + ['D', 'E', 'C', 'A'] + na*4,
    ...                     'class3': ['B', 'C'] + na*4 + ['C', 'C'] + na*2,
    ...                     'class4': na*2 + ['A', 'C'] + na*2 + ['A', 'A'] + na*2,
    ...                     'class5': na*4 + ['B', 'A'] + na*2 + ['A', 'C']})
    >>> cols = ['class%s'%x for x in range(1, 6)]
    >>> col_name = 'class'
    >>> col_val_name = 'grade'
    >>> df4 = df_cols2rows(df3, cols, col_name, col_val_name)
    >>> df5 = df_cols2rows(df3, cols, col_name, col_val_name,
    ...                    dropna=False)
    '''
    assert isinstance(cols, (list, tuple))
    idx_cols = [x for x in df.columns if not x in cols]
    df = df.set_index(idx_cols)
    df = df.stack(dropna=dropna)
    df = pd.DataFrame(df, columns=[col_val_name])
    df.index.names = idx_cols + [col_name]
    df = df.reset_index()
    return df


FullMethodType = NewType('FullMethodType',
                         Literal['product', 'pivot'])
FillMethodType = NewType('FillMethodType',
                         Literal['ffill', 'bfill',
                                 'ffillbfill', 'bfillffill'])

@beartype
def get_full_df(df: pd.DataFrame,
                full_col : str,
                fulls: Iterable,
                idcols: Union[str, List[str], None] = None,
                vcols: Union[str, List[str], None] = None,
                val_nan: Any = None,
                fill: Union[FillMethodType, None, bool] = 'ffill',
                fill_with_all: bool = True,
                final_dropna: bool = True,
                only_fulls: bool = True):
    '''
    df中full_col列的值扩充到fulls
    
    Example
    -------
    >>> df = pd.DataFrame({'t': [2, 3, 5, 7, 9],
    ...                    'a': ['x1', 'x1', 'x3', 'x4', 'x4'],
    ...                    'b': ['y1', 'y2', 'y3', 'y4', 'y4'],
    ...                    'c': ['z1', 'z1', 'z5', 'z7', 'z9']})
    >>> get_full_df(df, 't', range(1, 11))
    >>> get_full_df(df, 't', [2, 4, 5, 8, 10])
    >>> get_full_df(df, 't', range(1, 11), idcols='c')
    >>> get_full_df(df, 't', range(1, 11), idcols=['a', 'b'])
    >>> df['c'] = ['z1', 'z1', np.nan, np.nan, 'z9']
    >>> get_full_df(df, 't', range(1, 11), idcols=['a', 'b'], val_nan='npnan')
    >>> get_full_df(df, 't', [2, 5, 9, 10], idcols=['a', 'b'], val_nan='npnan', final_dropna=False)
    >>> get_full_df(df, 't', [2, 5, 9, 10], idcols=['a', 'b'], val_nan='npnan', final_dropna=True)
    '''
    if df.shape[0] == 0:
        return df
    idcols = check_list_arg(idcols, allow_none=True)
    vcols = check_list_arg(vcols, allow_none=True)
    def _fillna(df):
        if pd.__version__ < '2.1.0':
            if fill in ['ffill', 'bfill']:
                df = df.fillna(method=fill)
            elif fill == 'ffillbfill':
                df = df.fillna(method='ffill').fillna(method='bfill')
            elif fill == 'bfillffill':
                df = df.fillna(method='bfill').fillna(method='ffill')
        else:
            if fill in ['ffill', 'bfill']:
                df = eval('df.%s()'%fill)
            elif fill == 'ffillbfill':
                df = df.ffill().bfill()
            elif fill == 'bfillffill':
                df = df.bfill().ffill()
        return df
    if isnull(idcols):
        if isnull(vcols):
            vcols = [x for x in df.columns if x != full_col]
        df = df[[full_col]+vcols].copy()
        if not isnull(val_nan):
            for c in vcols:
                df[c] = df[c].fillna(val_nan)
        keepcol = get_tmp_new([full_col]+list(df.columns), 'keep', ext='_')
        res = pd.DataFrame({full_col: fulls, keepcol: 1})
        if not fill_with_all:
            res = pd.merge(res, df, how='left', on=full_col)
        else:
            res = pd.merge(res, df, how='outer', on=full_col)
        res = res.sort_values(full_col)
        res = _fillna(res)
        if final_dropna:
            res = res.dropna(subset=vcols)
    else:
        # 受影响的列
        if isnull(vcols):
            vcols = [x for x in df.columns if not x in idcols+[full_col]]
        assert all([not x in vcols for x in idcols])
        assert not full_col in vcols
        assert not full_col in idcols
        res = df[[full_col]+idcols+vcols].copy()
        if not isnull(val_nan):
            for c in vcols:
                res[c] = res[c].fillna(val_nan)
        oncols = [full_col]+idcols
        assert res[oncols].isna().sum().sum() == 0
        full = pd.DataFrame(
               product(fulls, *(res[c].unique() for c in idcols)),
               columns=oncols)
        keepcol = get_tmp_new(list(full.columns)+list(res.columns), 'keep', ext='_')
        full[keepcol] = 1
        if not fill_with_all:
            res = pd.merge(full, res, how='left', on=oncols)
        else:
            res = pd.merge(full, res, how='outer', on=oncols)
        res = res.sort_values(oncols)
        if pd.__version__ < '2.1.0':
            if fill in ['ffill', 'bfill']:
                res = res.groupby(idcols, as_index=False, group_keys=False).apply(
                      lambda x: x.fillna(method=fill))
            elif fill == 'ffillbfill':
                res = res.groupby(idcols, as_index=False, group_keys=False).apply(
                      lambda x: x.fillna(method='ffill').fillna(method='bfill'))
            elif fill == 'bfillffill':
                res = res.groupby(idcols, as_index=False, group_keys=False).apply(
                      lambda x: x.fillna(method='bfill').fillna(method='ffill'))
        else:
            if fill in ['ffill', 'bfill']:
                res = res.groupby(idcols, as_index=False, group_keys=False).apply(
                      lambda x: eval('x.%s()'%fill))
            elif fill == 'ffillbfill':
                res = res.groupby(idcols, as_index=False, group_keys=False).apply(
                      lambda x: x.ffill().bfill())
            elif fill == 'bfillffill':
                res = res.groupby(idcols, as_index=False, group_keys=False).apply(
                      lambda x: x.bfill().ffill())
        if final_dropna:
            res = res.dropna(subset=vcols, how='all')
    res = res.drop(keepcol, axis=1)
    if only_fulls:
        # TODO: 数据较大时用isin判断可能比较慢，改为通过临时变量删除处理
        res = res[res[full_col].isin(list(fulls))]
    res = res.reset_index(drop=True)
    return res


DateTimeType = NewType('DateTimeType',
                       Union[str,
                             datetime.datetime,
                             datetime.date]
                       )


# @beartype
def get_full_components_df(df: pd.DataFrame,
                           parent_col: str,
                           child_col: str,
                           tincol: str,
                           toutcol: str,
                           tfulls: Iterable,
                           toutnan: DateTimeType,
                           tcol_res: str = 'time',
                           keep_inout: bool = False
                           ):
    '''
    | 根据纳入、退出日期获取在给定时间内的所有成分
    
    Example
    -------
    >>> df = pd.DataFrame(
    ...      {'idxname': ['a', 'a', 'b', 'b', 'a', 'c', 'c'],
    ...       'stock': ['a1', 'a2', 'b1', 'b2', 'a3', 'c1', 'c2'],
    ...       'indate': ['20210101', '20210515', '20210405', '20210206',
    ...                  '20220307', '20220910', '20230409'],
    ...       'outdate': ['20220305', np.nan, np.nan, '20230209',
    ...                   np.nan, np.nan, '20230518']})
    >>> parent_col, child_col, tincol, toutcol = 'idxname', 'stock', 'indate', 'outdate'
    >>> from finfactory.fintools.utils_chn import get_dates_cond
    >>> tfulls = get_dates_cond('quarter_end', '20210101')
    >>> tfulls = [x.strftime('%Y%m%d') for x in tfulls]
    >>> toutnan = '20991231'
    >>> df1 = get_full_components_df(
    ...       df, parent_col, child_col, tincol, toutcol,
    ...       tfulls, toutnan, tcol_res='time')
    '''
    if df.shape[0] == 0:
        if keep_inout:
            df = df[[parent_col, child_col, tcol_res, tincol, toutcol]]
        else:
            df = df[[parent_col, child_col, tcol_res]]
    df = df[[parent_col, child_col, tincol, toutcol]].copy()
    df[toutcol] = df[toutcol].fillna(toutnan)
    tmp = df.to_dict(orient='split')['data']
    tmp = [tuple(x) for x in tmp]
    df = pd.DataFrame(np.ones((len(tfulls), len(tmp))), index=tfulls)
    df.index.name = tcol_res
    df.columns = tmp
    df = df.reset_index()
    df = df_cols2rows(df, tmp, 'tmp', 'IsIn')
    df[[parent_col, child_col, tincol, toutcol]] = df['tmp'].tolist()
    df = df[(df[tincol] <= df[tcol_res]) & (df[toutcol]>= df[tcol_res])]
    if keep_inout:
        df = df[[parent_col, child_col, tcol_res, tincol, toutcol]]
    else:
        df = df[[parent_col, child_col, tcol_res]]
    df = df.sort_values([parent_col, tcol_res, child_col])
    return df.reset_index(drop=True)


def get_first_appear(series, func_cond,
                     reverse=False,
                     return_iloc=False):
    '''
    | 获取满足func_cond(x)为True的值在series中第一次出现时的索引
    | 若reverse为True，则是最后一次出现
    | 若return_iloc为True，则返回行号和值，否则返回索引和值
    '''
    assert callable(func_cond)
    # df = pd.DataFrame({'s': series})
    # df['ok'] = df['s'].apply(lambda x: func_cond(x)).astype(int)
    # if return_iloc:
    #     df = df.reset_index(drop=True)
    # idx = -1 if reverse else 0
    # try:
    #     return df[df['ok'] == 1].index[idx], df[df['ok'] == 1]['ok'].iloc[idx]
    # except:
    #     return None, None
    if not reverse:
        n, k, find = len(series), 0, False
        while k < n and not find:
            find = func_cond(series.iloc[k])
            if find:
                if return_iloc:
                    return k, series.iloc[k]
                return series.index[k], series.iloc[k]
            k += 1
        return None, None
    else:
        k, find = len(series)-1, False
        while k > -1 and not find:
            find = func_cond(series.iloc[k])
            if find:
                if return_iloc:
                    return k, series.iloc[k]
                return series.index[k], series.iloc[k]
            k -= 1
        return None, None


def get_appear_order(series, ascending=True):
    '''
    标注series (`pandas.Series` , 离散值)中重复元素是第几次出现，
    
    返回为 `pandas.Series`，ascending设置返回结果是否按出现次序升序排列

    Examples
    --------
    >>> df = pd.DataFrame({'v': ['A', 'B', 'A', 'A', 'C', 'C']})
    >>> df.index = ['a', 'b', 'c', 'd', 'e', 'f']
    >>> df['nth'] = get_appear_order(df['v'], ascending=False)
    >>> df
       v  nth
    a  A    3
    b  B    1
    c  A    2
    d  A    1
    e  C    2
    f  C    1
    '''
    df = pd.DataFrame({'v': series})
    # df['Iidx'] = range(0, df.shape[0])
    # df['nth_appear'] = df.groupby('v')['Iidx'].rank(ascending=ascending)
    # df['nth_appear'] = df['nth_appear'].astype(int)
    df['nth_appear'] = df.groupby('v').cumcount(ascending=ascending) + 1
    return df['nth_appear']


def label_rep_index_str(df):
    '''
    `df (pandas.DataFrame)` 中的index若有重复，对重复的index进行后缀编号，返回新的 `pandas.DataFrame`

    .. note::
        若存在重复的index，则添加后缀编号之后返回的df，其index为str类型

    Examples
    --------
    >>> df = pd.DataFrame([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    >>> label_rep_index_str(df)
        0
    0   1
    1   2
    2   3
    3   4
    4   5
    5   6
    6   7
    7   8
    8   9
    9  10
    >>> df.index = [0, 0, 0, 1, 1, 2, 2, 2, 2, 3]
    >>> label_rep_index_str(df)
          0
    0     1
    0_2   2
    0_3   3
    1     4
    1_2   5
    2     6
    2_2   7
    2_3   8
    2_4   9
    3    10
    '''
    if df.index.duplicated().sum() == 0:
        return df
    else:
        df = df.copy()
        idx_name = df.index.name
        idx_tmp_col = get_tmp_col(df, '_tmp_idx_')
        df[idx_tmp_col] = df.index
        df[idx_tmp_col] = df[idx_tmp_col].astype(str)
        tmp_col = '_tmp_'
        df[tmp_col] = get_appear_order(df[idx_tmp_col])
        df[idx_tmp_col] = df[[idx_tmp_col, tmp_col]].apply(
            lambda x: x[idx_tmp_col] if x[tmp_col] == 1 else \
                      '{}_{}'.format(x[idx_tmp_col], x[tmp_col]),
                      axis=1)
        df.drop(tmp_col, axis=1, inplace=True)
        df.set_index(idx_tmp_col, inplace=True)
        df.index.name = idx_name
        return df


def drop_index_duplicates(df, keep='first'):
    '''删除 ``df (pandas.DataFrame)`` 中index重复的记录'''
    return df[~df.index.duplicated(keep=keep)]


def count_values(df, cols=None):
    '''计算df列中cols指定列的值出现次数'''
    if cols is None:
        cols = list(df.columns)
    elif isinstance(cols, str):
        cols = [cols]
    assert isinstance(cols, (list, tuple))
    tmp = df.reindex(columns=cols)
    tmp['count'] = 1
    tmp = tmp.groupby(cols, as_index=False)['count'].count()
    df_ = pd.merge(df, tmp, how='left', on=cols)
    df_.index = df.index
    return df_['count']


def count_index(df):
    '''计算df的每个index出现的次数'''
    df_index = pd.DataFrame({'index_': df.index})
    df_index['count'] = count_values(df_index, 'index_')
    df_index.index = df_index['index_']
    return df_index['count']


def get_all_turns(series):
    '''获取序列series中所有的转折点，返回series中-1位低点，1位高点'''
    s = series.copy()
    if s.name is None:
        s.name = 'series'
    if s.index.name is None:
        s.index.name = 'idx'
    df = pd.DataFrame(s)
    col = df.columns[0]
    df.reset_index(inplace=True)
    
    df['dif'] = df[col].diff()
    df['dif_big'] = (df['dif'] > 0).astype(int)
    df['dif_sml'] = -1 * (df['dif'] < 0).astype(int)
    ktmp = 1
    while ktmp < df.shape[0] and df.loc[df.index[ktmp], 'dif'] == 0:
        ktmp += 1
    if df.loc[df.index[ktmp], 'dif'] > 0:
        df.loc[df.index[0], 'dif_sml'] = -1
    elif df.loc[df.index[ktmp], 'dif'] < 0:
        df.loc[df.index[0], 'dif_big'] = 1
    df['label'] = df['dif_big'] + df['dif_sml']
    label_ = replace_repeat_pd(df['label'][::-1], 1, 0)
    label_ = replace_repeat_pd(label_, -1, 0)
    df['label'] = label_[::-1]
    
    df.set_index(s.index.name, inplace=True)
    
    return df['label']


def group_shift():
    '''分组shift，待实现'''
    raise NotImplementedError
    
    
def rolling_corr(df, col1, col2, *args, **kwargs):
    '''滚动相关性（2个变量）'''
    raise NotImplementedError
    # res = df[[col1, col2]].rolling(*args, **kwargs).corr()
    # res = res.reset_index()
    # res = res[res['level_1'] == col1][col2]
    # df['corr'] = res.values
    # return df
    
    
def group_fillna(df, col_fill, cols_groupby, return_all=False,
                 **kwargs_fillna):
    '''
    分组缺失值填充
    '''
    if isinstance(cols_groupby, str):
        cols_groupby = [cols_groupby]
    series_fill = df.groupby(cols_groupby)[col_fill].fillna(**kwargs_fillna)
    series_fill.index = df.index
    return series_fill
    

def group_rank(df, col_rank, cols_groupby,
               return_all=False, **kwargs_rank):
    '''
    分组排序
    
    对df(`pandas.DataFrame`)中 ``cols_rank`` 指定列按 ``cols_groupby`` 指定列分组排序
    
    TODO
    ----
    col_rank可为列表，此时返回dataframe，return_all设置只返回指定列结果或者返回全部dataframe
    
    Parameters
    ----------
    df : pandas.DataFrame
        待排序数据表
    col_rank : str
        需要排序的列
    cols_groupby : str, list
        分组依据列
    **kwargs_rank :
        pandas中rank函数接受的参数
    
    Returns
    -------
    series_rank : pandas.Series
        排序结果
    '''
    assert isinstance(col_rank, str), '`cols_rank`必须为str'
    assert isinstance(cols_groupby, (str, list)), '`cols_groupby`必须为str或list'
    if isinstance(cols_groupby, str):
        cols_groupby = [cols_groupby]
    series_rank = df.groupby(cols_groupby)[col_rank].rank(**kwargs_rank)
    series_rank.index = df.index
    return series_rank


def get_func_df_concat(func, args_kwargs_list, concat_axis=0):
    '''
    | func(args, \**kwargs)作用于args_kwargs_list中的参数，将所有结果concat返回
    | func函数返回值必须为pd.DataFrame
    
    Examples
    --------
    >>> func = lambda x, y, z: pd.DataFrame({'a': [x, y, z]})
    >>> args_kwargs_list = [[(1, 2), {'z': 3}],
    ...                     [(2, 3), {'z': 4}]]
    >>> get_func_df_concat(func, args_kwargs_list)
       a
    0  1
    1  2
    2  3
    0  2
    1  3
    2  4
    '''
    data = []
    for args, kwargs in args_kwargs_list:
        data.append(func(*args, **kwargs))
    return pd.concat(data, axis=concat_axis)


def df_groupby_func(df, by_cols, func,
                    as_index=False, group_keys=False,
                    reset_index='drop',
                    *args_func, **kwargs_func):
    '''
    TODO
    ----
    - by_cols中有nan时的检查和处理
    - group_keys和as_index的异同检查确认
    
    | df按by_cols分组作用于func(x, \*args, \**kwargs)函数
    | reset_index:
    |   若为drop，则重置返回的index
    |   若为False，则不处理groupby之后的index
    |   若为ori，如返回数据与原始df行数相同，则使用原始index，否则不处理groupby之后的index
    | 解决groupby.apply出现执行多次的问题(貌似pandas更新到1.5.0之后没出现了)，参考:
    | http://t.zoukankan.com/wkang-p-10150401.html
    '''
    assert reset_index in ['drop', 'ori', False]
    n = df.shape[0]
    # data = df.groupby(by_cols, as_index=as_index).apply(
    #                   lambda x: func(x, *args_func, **kwargs_func))
    data = df.groupby(by_cols, group_keys=group_keys).apply(
                      lambda x: func(x, *args_func, **kwargs_func))
    if not reset_index:
        return data
    if reset_index == 'drop':
        return data.reset_index(drop=True)
    if reset_index == 'ori':
        if data.shape[0] == n:
            data.index = df.index
        return data
    return data


def move_cols_to(df, cols, dirt='start'):
    '''将df中cols指定列移动到表格的最前面(dirt='start')或最后面(dirt='end')'''
    assert dirt in ['start', 'end'], '`dirt`只能为`start`或`end`'
    cols = check_list_arg(cols)
    cols_ = [x for x in df.columns if x not in cols]
    if dirt == 'start':
        return df[cols+cols_]
    else:
        return df[cols_+cols]


def bootstrapping():
    '''
    bootstraping, 待实现
    '''
    raise NotImplementedError


def groupby_rolling_func(data, cols_groupby, cols_val, func, keep_index=True,
                         kwargs_rolling={}, kwargs_func={}):
    '''
    data按照cols_groupby分组，然后在cols_val列上rolling调用func，    
    func的参数通过kwargs_func设定，
    若cols_val为str，则返回pd.Series；若为list，则返回pd.DataFrame
    若keep_index为True，则返回结果中的index与data一样，否则返回结果中的index由
    cols_groupby设定
    '''
    # if isinstance(cols_groupby, str):
    #     cols_groupby = [cols_groupby]
    # cols = [cols_val] if isinstance(cols_val, str) else cols_val
    # df = data.reindex(columns=cols_groupby+cols)
    raise NotImplementedError
    
    
def merge_dicts(dicts: Union[List[dict], tuple]):
    '''
    | 将多个字典合并成一个字典
    | 注意：若字典中key相同，则合并之后前面的值会被后面的值更新覆盖
    '''
    assert isinstance(dicts, (list, tuple))
    assert all([isinstance(x, dict) for x in dicts])
    res = {}
    for d in dicts:
        res.update(d)
    return res


@beartype
def get_new_literal_type(
        name: str,
        l: Union[List[Union[str, int, float]]]
        ):
    '''按l指定值的范围生成一个新的类型，类型名为name'''
    allows = ', '.join(["'%s'"%x 
                        if isinstance(x, str) else "%s"%x
                        for x in l])
    allows = 'Literal[{}]'.format(allows)
    allows = eval(allows)
    return NewType(name, allows)


_DictActType = get_new_literal_type(
    '_DictActType', ['+', '-', '*', '/', '**'])

@beartype
def merge_dicts_act(dicts: Union[List[dict]],
                    act: str):
    '''
    按act指定方式进行字典合并，act支持_DictActType中指定的操作类型
    
    Examples
    --------
    >>> dicts = [{'a': 1, 'b': 2}, {'a': 2, 'b': 3}, {'c': 4}]
    >>> merge_dicts_act(dicts, '+')
    {'a': 3, 'b': 5, 'c': 4}
    >>> merge_dicts_act(dicts, '*')
    {'a': 2, 'b': 6, 'c': 4}
    >>> merge_dicts_act(dicts, '**')
    {'a': 1, 'b': 8, 'c': 4}
    '''
    res = {}
    for d in dicts:
        for k, v in d.items():
            if k not in res:
                res[k] = v
            else:
                exec('res[k] %s= v'%act)
    return res


def link_lists(lists: List[list]):
    '''
    | 将多个列表连接成一个列表
    | 注：lists为列表，其每个元素也为一个列表
    
    Examples
    --------
    >>> a = [1, 2, 3]
    >>> b = [4, 5, 6]
    >>> c = ['a', 'b']
    >>> d = [a, b]
    >>> link_lists([a, b, c, d])
    [1, 2, 3, 4, 5, 6, 'a', 'b', [1, 2, 3], [4, 5, 6]]
    '''
    assert isinstance(lists, (list, tuple))
    assert all([isinstance(x, (list, tuple)) for x in lists])
    newlist = []
    for item in lists:
        newlist.extend(item)
    return newlist


def get_lists_inter(lists: List[Union[list, tuple]]):
    '''获取多个列表的交集'''
    assert isinstance(lists, (list, tuple))
    assert all([isinstance(x, (list, tuple)) for x in lists])
    res = set(lists[0])
    for x in lists[1:]:
        res = res.intersection(set(x))
    return list(res)


def list_eq(l1: list, l2: list, order=True):
    '''判断两个列表l1和l2是否相等，若orde为False，则只要元素相同即判断为相等'''
    if order:
        return operator.eq(l1, l2)
    return set(l1) == set(l2)


def remove_list_idxs(l: list, idxs: List[int]):
    '''删除列表l中idxs所有索引数据'''
    idxs.sort()
    ndel = 0
    for k in range(len(idxs)):
        i = idxs[k]
        l.pop(i-ndel)
        ndel += 1
    return l


def get_num_decimal(x, ignore_tail0=True):
    '''
    | 获取浮点数x的小数位数
    | ignore_tail0设置是否忽略小数点尾部无效的0
    '''
    try:
        float(x)
    except:
        raise ValueError('输入不是有效浮点数，请检查：{}！'.format(x))
    xstr = str(x)
    xsplit = xstr.split('.')
    if len(xsplit) == 1:
        return 0
    if len(xsplit) > 2:
        raise ValueError('输入出错，请检查：{}！'.format(xstr))
    decimal = xsplit[-1]
    if ignore_tail0:
        while decimal[-1] == '0':
            decimal = decimal[:-1]
    return len(decimal)


def list2dict(list_key, list_val):
    '''两个列表生成字典'''
    return dict(zip(list_key, list_val))


def sort_dict(d, by='key', reverse=False):
    '''
    对字典排序，by设置依据'key'还是'value'排，reverse同sorted函数参数
    '''
    assert by in ['key', 'value']
    if by == 'key':
        d_ = sorted(d.items(), key=lambda kv: (kv[0], kv[1]), reverse=reverse)
    else:
        d_ = sorted(d.items(), key=lambda kv: (kv[1], kv[0]), reverse=reverse)
    return dict(d_)


def insert_into_list(l, val, loc_val, dirt='before'):
    '''在列表l中的loc_val前或后插入val'''
    res = l.copy()
    assert dirt in ['before', 'after']
    idx = res.index(loc_val)
    if dirt == 'before':
        res.insert(idx, val)
    else:
        res.insert(idx+1, val)
    return res


def count_list(l):
    '''对l中的元素计数，返回dict'''
    # return dict(Counter(l))
    return Counter(l)


def _get_label_bins_range(bins, labels):
    assert len(labels) == (len(bins)-1)
    res = {}
    for k in range(len(labels)):
        l = labels[k]
        res[l] = (bins[k], bins[k+1])
    return res


def get_label_bins_range(bins, labels,
                         left_close=False,
                         right_close=False):
    assert isinstance(bins, (list, tuple))
    assert isinstance(labels, (list, tuple))
    if (not left_close) and (not right_close):
        assert len(labels) == (len(bins)+1)
        return _get_label_bins_range(
                [-np.inf]+bins+[np.inf], labels)
    elif left_close and right_close:
        return _get_label_bins_range(bins, labels)
    else:
        assert len(labels) == len(bins)
        if left_close:
            return _get_label_bins_range(bins+[np.inf], labels)
        else:
            return _get_label_bins_range([-np.inf]+bins, labels)
    

def tmprint(*args, flush=False, **kwargs):
    if not flush:
        print(*args, **kwargs)
        print('    [time: {}]'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    else:
        print_str = ' '.join([str(x) for x in args]) + ' - [time: {}]'.format(
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        print('\r', print_str, end='', flush=True)
    
def fmt(fstr, *args, **kwargs):
    return fstr.format(*args, **kwargs)


def url2chn(url):
    '''将url中的中文乱码（实际上为utf-8）转化为正常url'''
    return urllib.parse.unquote(url)


def replace_con_blank(string, to):
    '''将string中连续空格替换为to指定字符'''
    return re.sub(' +', to, string)


def change_dict_key(d, func_key_map):
    '''修改字典d中的key值，即d[k]=v变成d[func_key_map(k)]=v'''
    return {func_key_map(k): v for k, v in d.items()}


def get_func_source_code(func):
    '''获取func函数的源代码'''
    return inspect.getsource(func)


def get_func_arg_info(func):
    '''
    获取函数func的参数信息
    
    Examples
    --------
    >>> def func(a:int, b, c:float=1.0, c1=2, *args,
    ...          e, d=2, **kwargs):
    ...     pass
    >>> get_func_arg_info(func)
    {'args': ['a', 'b', 'c', 'c1'],
     'argdefaults': {'c': 1.0, 'c1': 2},
     'varargs': 'args',
     'varkw': 'kwargs',
     'kwonlyargs': ['e', 'd'],
     'kwonlydefaults': {'d': 2},
     'annotations': {'a': int, 'c': float}}
    '''
    all_ = inspect.getfullargspec(func)
    res = {'args': all_.args,
           'argdefaults': all_.defaults,
           'varargs': all_.varargs,
           'varkw': all_.varkw,
           'kwonlyargs': all_.kwonlyargs,
           'kwonlydefaults': all_.kwonlydefaults,
           'annotations': all_.annotations}
    if not isnull(all_.defaults):
        n_argdefaults = len(all_.defaults)
        argdefaults = all_.args[-n_argdefaults:]
        res['argdefaults'] = dict(zip(argdefaults, all_.defaults))
    return res


def parse_args(args_info, description=None):
    '''
    命令行参数解析
    
    Parameters
    ----------
    args_info : list, dict
        | 参数信息
        | 若无分组，格式为:
        |     [(['-a', '--arg1', ...], {'type': int, 'default': 1, ...}),
        |      (['-b', ...], {...}),
        |      ...]
        | 若有分组，格式为:
        |     {'groupname1':
        |         [(['-a', '--arg1', ...], {'type': int, 'default': 1, ...}),
        |          (['-b', ...], {...}),
        |          ...],
        |      'groupname2': [...], ...}        
    '''
    parser = argparse.ArgumentParser(description=description)
    group = isinstance(args_info, dict)
    if not group:
        for args, kwargs in args_info:
            parser.add_argument(*args, **kwargs)
    else:
        for gname, gargs_info in args_info.items():
            g = parser.add_argument_group(gname)
            for args, kwargs in gargs_info:
                g.add_argument(*args, **kwargs)
    return parser


def gen_args_praser(func,
                    native_eval_types=('list', 'tuple', 'dict')):
    '''
    生成func函数的参数解析
    '''
    func_args = get_func_arg_info(func)
    args_info = []
    if not isnull(func_args['argdefaults']):
        requireds = [x for x in func_args['args'] if x not in func_args['argdefaults']]
        defaults = func_args['argdefaults'].copy()
    else:
        requireds = func_args['args']
        defaults = {}
    if not isnull(func_args['kwonlydefaults']):
        requireds += [x for x in func_args['kwonlyargs'] if x not in func_args['kwonlydefaults']]
        defaults.update(func_args['kwonlydefaults'])
    else:
        requireds += func_args['kwonlyargs']
    for arg in requireds:
        if arg not in func_args['annotations']:
            args_info.append((['--%s'%arg], {'required': True}))
        else:
            # if func_args['annotations'][arg].__name__.lower() == 'list':
            #     # 传参命令写法：--arg l1 l2 l3
            #     # 会解析成文本列表：arg = ['l1', 'l2', 'l3']
            #     args_info.append((['--%s'%arg], {'required': True, 'nargs': '+'}))
            if func_args['annotations'][arg].__name__.lower()  in native_eval_types:
                # 传参命令写法：按照python正常写法即可，但是不能有空格，如：
                # list: --arg ['a',2,{'a':3}]
                # tuple: --arg ('a',2,{'a':3})
                # dict: --arg {'k1':'v1','k2':2}
                args_info.append((['--%s'%arg], {'required': True, 'type': lambda x: eval(x), 'help': '入参按照python正常写法写，但是不能有空格。'}))
            else:
                args_info.append((['--%s'%arg], {'required': True, 'type': func_args['annotations'][arg]}))
    for arg, default in defaults.items():
        if not arg in func_args['annotations']:
            args_info.append((['--%s'%arg], {'default': default}))
        else:
            if func_args['annotations'][arg].__name__ == 'bool':
                if not default:
                    args_info.append((['--%s'%arg], {'action': 'store_true', 'default': default}))
                else:
                    args_info.append((['--%s'%arg], {'action': 'store_false', 'default': default}))
            elif func_args['annotations'][arg].__name__.lower()  in native_eval_types:
                args_info.append((['--%s'%arg], {'default': default, 'type': lambda x: eval(x), 'help': '入参按照python正常写法写，但是不能有空格。'}))
            else:
                args_info.append((['--%s'%arg], {'default': default, 'type': func_args['annotations'][arg]}))
    # kwargs，按字典处理
    if not isnull(func_args['varkw']):
        args_info.append((['--%s'%func_args['varkw']], {'default': {}, 'type': lambda x: eval(x), 'help': '入参按照python正常写法写，但是不能有空格。'}))
    return parse_args(args_info), func_args


def get_topn_names(df, n=1, max_or_min='max',
                   col_or_row='col'):
    '''
    获取df中值最大/小的前n列/行的名称
    
    Examples
    --------
    >>> d = {'A': [30, 2, 6, 4, 5],
    ...      'B': [6, 7, 80, 5, 10],
    ...      'C': [11, 12, 13, 14, 15],
    ...      'D': [16, 17, 18, 19, 20],
    ...      'E': [21, 22, 23, 24, 25]}
    >>> df = pd.DataFrame(d, index=['a', 'b', 'c', 'd', 'e'])
    >>> res = get_topn_names(df, n=2)
    >>> res1 = get_topn_names(df, n=2, col_or_row='row')
    '''
    assert max_or_min.lower() in ['max', 'min']
    assert col_or_row.lower() in ['col', 'row']
    axis = 1 if col_or_row.lower() == 'col' else 0
    if max_or_min.lower() == 'max':
        res = df.apply(lambda x:
                 x.nlargest(n).index.tolist(), axis=axis)
    else:
        res = df.apply(lambda x:
                 x.nsmallest(n).index.tolist(), axis=axis)
    return res


def text2bytestream(text: str,
                    chunksize: int = 10,
                    timegap: Union[int, float] = None):
    '''
    Examples
    --------
    >>> import pickle
    >>> text = 'xxxxxxxqqqqqqq1111111'
    >>> a = text2bytestream(text, timegap=1)
    >>> for x in a:
    ...     print(type(x))
    # ...     y = pickle.loads(x)
    ...     y = x.decode('utf-8')
    ...     print(type(y), y)
    '''
    iend = chunksize
    while iend <= len(text):
        tgt = text[iend-chunksize:iend]
        iend += chunksize
        # import pickle
        # yield pickle.dumps(tgt)
        yield tgt.encode('utf-8')
        if timegap:
            time.sleep(timegap)
    

if __name__ == '__main__':
    from finfactory.fintools.fintools import cci
    from dramkit import load_csv, plot_series
    
    tr = TimeRecoder()
    def test():
        # 50ETF日线行情------------------------------------------------------------
        fpath = './_test/510050.SH_daily_qfq.csv'
        data = load_csv(fpath)
        data.set_index('date', drop=False, inplace=True)
        data.index.name = 'time'
    
        data['cci'] = cci(data)
        data['cci_100'] = data['cci'].apply(lambda x: 1 if x > 100 else \
                                                        (-1 if x < -100 else 0))
    
        plot_series(data.iloc[-200:, :], {'close': ('.-k', False)},
                    cols_styl_low_left={'cci': ('.-c', False)},
                    cols_to_label_info={'cci':
                                    [['cci_100', (-1, 1), ('r^', 'bv'), False]]},
                    xparls_info={'cci': [(100, 'r', '-', 1.3),
                                         (-100, 'r', '-', 1.3)]},
                    figsize=(8, 7), grids=True)
    
        start_ends_1 = get_con_start_end(data['cci_100'], lambda x: x == -1)
        start_ends1 = get_con_start_end(data['cci_100'], lambda x: x == 1)
        data['cci_100_'] = 0
        for start, end in start_ends_1:
            if end+1 < data.shape[0]:
                data.loc[data.index[end+1], 'cci_100_'] = -1
        for start, end in start_ends1:
            if end+1 < data.shape[0]:
                data.loc[data.index[end+1], 'cci_100_'] = 1
    
        plot_series(data.iloc[-200:, :], {'close': ('.-k', False)},
                    cols_styl_low_left={'cci': ('.-c', False)},
                    cols_to_label_info={'cci':
                                    [['cci_100_', (-1, 1), ('r^', 'bv'), False]],
                                        'close':
                                    [['cci_100_', (-1, 1), ('r^', 'bv'), False]]},
                    xparls_info={'cci': [(100, 'r', '-', 1.3),
                                         (-100, 'r', '-', 1.3)]},
                    figsize=(8, 7), grids=True)
        return data
    # res = test()
    tr.used()
