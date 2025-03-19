# -*- coding: utf-8 -*-
# HuYueyong, 2024

"""ZigZag算法（拐点识别）"""

#%%
import logging
from dataclasses import dataclass
import numpy as np
from dramkit.const import (
    SeriesType,
    NumOrNoneType,
    FloatOrNoneType,
    IntOrNoneType
)
from dramkit.gentools import (
    isna,
    catch_error,
    catch_warnings,
    raise_warn,
    cal_pct,
    _get_out2
)

# _MAX = sys.maxsize
_MAX = np.inf


@dataclass
class ZigZagParams(object):
    t_min: IntOrNoneType = None #  默认0
    pct_min: FloatOrNoneType = None  # eg. 1/100，默认0.0
    val_min: NumOrNoneType = None
    t_max: IntOrNoneType = None  # 默认_MAX
    pct_max: FloatOrNoneType = None
    val_max: NumOrNoneType = None
    t_min_up: IntOrNoneType = None
    t_min_down: IntOrNoneType = None
    t_max_up: IntOrNoneType = None
    t_max_down: IntOrNoneType = None
    pct_min_up: FloatOrNoneType = None  # eg. 1/100
    pct_min_down: FloatOrNoneType = None  # eg. -1/100
    pct_max_up: FloatOrNoneType = None
    pct_max_down: FloatOrNoneType = None
    val_min_up: NumOrNoneType = None
    val_min_down: NumOrNoneType = None
    val_max_up: NumOrNoneType = None
    val_max_down: NumOrNoneType = None
    zigzag: SeriesType = None
    pct_v00: float = 1.0
    logger: logging.Logger = None
    
    def check(self):
        """参数转化和检查"""
        if isna(self.t_min) and isna(self.t_min_up) and isna(self.t_min_down):
            self.t_min = 0
        if isna(self.t_max) and isna(self.t_max_up) and isna(self.t_max_down):
            self.t_max = _MAX
        if isna(self.pct_min) and \
           isna(self.pct_min_up) and isna(self.pct_min_down) and \
           isna(self.val_min_up) and isna(self.val_min_down):
            self.pct_min = 0.0
        
        self.t_min_up = self.t_min if isna(self.t_min_up) else self.t_min_up
        self.t_min_down = self.t_min if isna(self.t_min_down) else self.t_min_down
        self.t_max_up = self.t_max if isna(self.t_max_up) else self.t_max_up
        self.t_max_down = self.t_max if isna(self.t_max_down) else self.t_max_down
        self.pct_min_up = self.pct_min if isna(self.pct_min_up) else self.pct_min_up
        self.pct_max_up = self.pct_max if isna(self.pct_max_up) else self.pct_max_up
        self.val_min_up = self.val_min if isna(self.val_min_up) else self.val_min_up
        self.val_max_up = self.val_max if isna(self.val_max_up) else self.val_max_up
        self.pct_min_down = -1*self.pct_min if (isna(self.pct_min_down) and (not isna(self.pct_min))) else self.pct_min_down
        self.pct_max_down = -1*self.pct_max if (isna(self.pct_max_down) and (not isna(self.pct_max))) else self.pct_max_down
        self.val_min_down = -1*self.val_min if (isna(self.val_min_down) and (not isna(self.val_min))) else self.val_min_down
        self.val_max_down = -1*self.val_max if (isna(self.val_max_down) and (not isna(self.val_max))) else self.val_max_down
        
        # 最小间隔点参数（默认满足：t < t_min）
        for arg in ['t_min_up', 't_min_down']:
            arg_val = eval('self.%s'%arg)
            if isna(arg_val) or arg_val < 0:
                raise_warn('ZigZagParamWarn', '转折点之间的最小间隔点参数`{}`将设置为0！'.format(arg))
                exec('self.%s = 0'%arg)
                
        # 最大间隔点参数（默认不满足：t > t_max）
        for arg in ['t_max_up', 't_max_down']:
            arg_val = eval('self.%s'%arg)
            if isna(arg_val) or arg_val < 0:
                raise_warn('ZigZagParamWarn', '转折点之间的最大间隔点参数`{}`将设置为无穷大！'.format(arg))
                exec('self.%s = _MAX'%arg)
                
        # 上涨-长时最小幅度参数（默认满足：pct > pct_min_up and val > val_min_up）
        if not isna(self.pct_min_up) and not isna(self.val_min_up):
            raise_warn('ZigZagParamWarn', '同时设置`pct_min_up`和`val_min_up`，以`pct_min_up`为准！')
            self.val_min_up = -_MAX
        elif isna(self.pct_min_up) and isna(self.val_min_up):
            raise_warn('ZigZagParamWarn', '`pct_min_up`和`val_min_up`均未设置！')
            self.pct_min_up = self.val_min_up = -_MAX
        elif isna(self.pct_min_up):
            self.pct_min_up = -_MAX
        elif isna(self.val_min_up):
            self.val_min_up = -_MAX

        # 上涨-短时最大幅度参数（默认不满足：pct > pct_max_up or val > val_max_up）
        if not isna(self.pct_max_up) and not isna(self.val_max_up):
            raise_warn('ZigZagParamWarn', '同时设置`pct_max_up`和`val_max_up`，以`pct_max_up`为准！')
            self.val_max_up = _MAX
        elif isna(self.pct_max_up) and isna(self.val_max_up):
            self.pct_max_up = self.val_max_up = _MAX
        elif isna(self.pct_max_up):
            self.pct_max_up = _MAX
        elif isna(self.val_max_up):
            self.val_max_up = _MAX
        
        # 下跌-长时最小幅度参数（默认满足：pct < pct_min_down and val < val_min_down）
        if not isna(self.pct_min_down) and not isna(self.val_min_down):
            raise_warn('ZigZagParamWarn', '同时设置`pct_min_down`和`val_min_down`，以`pct_min_down`为准！')
            self.val_min_down = _MAX
        elif isna(self.pct_min_down) and isna(self.val_min_down):
            raise_warn('ZigZagParamWarn', '`pct_min_down`和`val_min_down`均未设置！')
            self.pct_min_down = self.val_min_down = _MAX
        elif isna(self.pct_min_down):
            self.pct_min_down = _MAX
        elif isna(self.val_min_down):
            self.val_min_down = _MAX
        
        # 下跌-短时最大幅度参数（默认不满足：pct < pct_max_down or val < val_max_down）
        if not isna(self.pct_max_down) and not isna(self.val_max_down):
            raise_warn('ZigZagParamWarn', '同时设置`pct_max_down`和`val_max_down`，以`pct_max_down`为准！')
            self.val_max_down = -_MAX
        elif isna(self.pct_max_down) and isna(self.val_max_down):
            self.pct_max_down = self.val_max_down = -_MAX
        elif isna(self.pct_max_down):
            self.pct_max_down = -_MAX
        elif isna(self.val_max_down):
            self.val_max_down = -_MAX
            
        return self


@catch_warnings()
@catch_error()
def find_zigzag(high: SeriesType,
                low: SeriesType,
                *args,
                **kwargs
                ) -> SeriesType:
    """ZigZag转折点
    
    条件1：转折点之间的间隔点数大于等于t_max（默认参数为不满足）
    条件2：转折点之间的间隔点数大于等于t_min（默认参数为满足）
    条件3：转折点之间变化幅度大于等于pct_min或val_min（默认参数为满足）
    条件4：转折点之间变化幅度大于等于pct_max或val_max（默认参数为不满足）
    转折点确认条件：
        条件1 or (条件2 and 条件3) or ((not 条件2) and 条件4)

    Parameters
    ----------        
    high : SeriesType
        high序列数据
    low : SeriesType
        low序列数据
    t_min : int
        转折点之间的最小时间距离（间隔点的个数）
    pct_min : float
        在满足t_min参数设置的条件下，转折点和上一个转折点的最小变化百分比
        （应为正数，如1/100）
    val_min : float
        在满足t_min参数设置的条件下，转折点和上一个转折点的最小变化绝对值
        （若pct_min设置，则此参数失效）
    t_max : int
        转折点之间的最大时间距离若超过t_max，即视为满足转折条件
    pct_max : float
        在不满足t_min参数设置的条件下，转折点和上一个转折点的变化百分比若超过此参数值，则视为满足转折条件
    val_max : float
        在不满足t_min参数设置的条件下，转折点和上一个转折点的变化绝对值若超过此参数值，则视为满足转折条件
        （若pct_max设置，则此参数失效）
    t_min_up : int
        同 `t_min` ，只控制上涨
    t_min_down : int
        同 `t_min` ，只控制下跌
    t_max_up : int
        同 `t_max` ，只控制上涨
    t_max_down : int
        同 `t_max` ，只控制下跌
    pct_min_up : float
        同 `pct_min` ，只控制上涨
    pct_min_down : float
        同 `pct_min` ，只控制下跌（应为负数，如-1/100）
    pct_max_up : float
        同 `pct_max` ，只控制上涨
    pct_max_down : float
        同 `pct_max` ，只控制下跌
    val_min_up : float
        同 `val_min` ，只控制上涨
    val_min_down : float
        同 `val_min` ，只控制下跌
    val_max_up : float
        同 `val_max` ，只控制上涨
    val_max_down : float
        同 `val_max` ，只控制下跌
    zigzag : SeriesType
        可传入已有的zigzag结果，会寻找最近一个转折点确定的位置，然后增量往后计算
    pct_v00 : float
        计算百分比时分母为0指定结果
    logger : logging.Logger
        日志记录器

    Returns
    -------
    zigzag : SeriesType
        返回zigzag标签序列，其中1|-1表示确定的高|低点；5|-5表示未达到偏离条件而不能确定的高低点。
    """
    
    params = ZigZagParams(*args, **kwargs)
    params.check()
    
    high_ = high.copy()
    high, low = np.array(high), np.array(low)
    
    # 无效值检查
    assert np.isnan(high).sum() == 0, '`high`检测到无效值，请检查数据！'
    assert (high == np.inf).sum() == 0, '`high`检测到无穷大值，请检查数据！'
    assert (high == -np.inf).sum() == 0, '`high`检测到负无穷大值，请检查数据！'
    assert np.isnan(low).sum() == 0, '`low`检测到无效值，请检查数据！'
    assert (low == np.inf).sum() == 0, '`low`检测到无穷大值，请检查数据！'
    assert (low == -np.inf).sum() == 0, '`low`检测到负无穷大值，请检查数据！'
    
    n = len(high)
    if not isna(params.zigzag):
        zz = params.zigzag.copy()
    else:
        zz = np.zeros_like(high)
    
    def __cal_dif(v0, v1):
        pct, val = cal_pct(v0, v1, params.pct_v00), v1 - v0
        return pct, val
    
    def __up_sure(pct, val, t):
        cond1 = t >= params.t_max_up
        cond2 = t >= params.t_min_up
        cond3 = pct >= params.pct_min_up and val >= params.val_min_up
        cond4 = pct >= params.pct_max_up or val >= params.val_max_up
        cond = cond1 or (cond2 and cond3) or ((not cond2) and cond4)
        return cond
    
    def __down_sure(pct, val, t):
        cond1 = t >= params.t_max_up
        cond2 = t >= params.t_min_up
        cond3 = pct <= params.pct_min_down and val <= params.val_min_down
        cond4 = pct <= params.pct_max_down or val <= params.val_max_down
        cond = cond1 or (cond2 and cond3) or ((not cond2) and cond4)
        return cond
    
    def __confirm_high_from_ensure_low(k):
        """从前一个已确定的低点位置k开始确定下一个高点位置"""
        k0 = k
        v0 = low[k]
        
        up_sure, updown_sure = False, False
        
        cmax, cmax_idx = v0, k
        cmaxcmin = v0
        up_pct, up_val, t_up = -_MAX, -_MAX, -_MAX
        updown_pct, updown_val, t_updown = _MAX, _MAX, -_MAX
        
        k += 1
        print('TODO: 改为从k+2开始，因为要排除同一个时间点high和low相比的情况')
        while k < n and (not up_sure or not updown_sure):
            if low[k] < v0:
                cmax_idx = high[k0:k+1].argmax()
                return cmax_idx+k0, True, True
            
            if high[k] > cmax:
                cmax = high[k]
                cmax_idx = k
                cmaxcmin = cmax
                
                up_pct, up_val = __cal_dif(v0, cmax)
                t_up = cmax_idx - k0
            
            if low[k] <= cmaxcmin:
                cmaxcmin = low[k]
                updown_pct, updown_val = __cal_dif(cmax, cmaxcmin)
                t_updown = k - cmax_idx
                
            up_sure = __up_sure(up_pct, up_val, t_up)
            updown_sure = __down_sure(updown_pct, updown_val, t_updown)

            k += 1

        return cmax_idx, up_sure, updown_sure
    
    def __confirm_low_from_ensure_high(k):
        """从前一个已确定的高点位置k开始确定下一个低点位置"""
        k0 = k
        v0 = high[k]
        
        down_sure, downup_sure = False, False
        
        cmin, cmin_idx = v0, k
        cmincmax = v0
        down_pct, down_val, t_down = _MAX, _MAX, -_MAX
        downup_pct, downup_val, t_downup = -_MAX, -_MAX, -_MAX
        
        k += 1
        while k < n and (not down_sure or not downup_sure):
            if high[k] > v0:
                cmin_idx = low[k0:k+1].argmin()
                return cmin_idx+k0, True, True
            
            if low[k] < cmin:
                cmin = low[k]
                cmin_idx = k
                cmincmax = cmin
                
                down_pct, down_val = __cal_dif(v0, cmin)
                t_down = cmin_idx - k0
            
            if high[k] >= cmincmax:
                cmincmax = high[k]
                downup_pct, downup_val = __cal_dif(cmin, cmincmax)
                t_downup = k - cmin_idx
                
            down_sure = __down_sure(down_pct, down_val, t_down)
            downup_sure = __up_sure(downup_pct, downup_val, t_downup)

            k += 1

        return cmin_idx, down_sure, downup_sure
    
    def __update_zz_from_ensure(k, ktype, zz):
        """从已经确认的转折点k处往后计算所有转折点，更新zz"""
        assert ktype in [1, -1], '`ktype`只能为-1或1！'
        while k < n:
            if ktype == -1:
                func_confirm = __confirm_high_from_ensure_low
            else:
                func_confirm = __confirm_low_from_ensure_high
            k, ok_mid, ok_right = func_confirm(k)
            if ok_mid and ok_right:
                zz[k] = -ktype
                ktype = -ktype
            elif ok_mid and not ok_right:
                zz[k] = -ktype * 5
                break
            else:
                break
        return zz
    
    def __get_init_up_first():
        cmax_idx, cmax = 0, high[0]
        cmin, down_sure = _MAX, False
        down_pct, down_val, t_down = _MAX, _MAX, -_MAX
        k = 1
        while k < n and not down_sure:
            if high[k] > cmax:
                cmax_idx, cmax = k, high[k]
                cmin = _MAX
            if low[k] <= cmin:
                cmin = low[k]
                down_pct, down_val = __cal_dif(cmax, cmin)
                t_down = k - cmax_idx
            down_sure = __down_sure(down_pct, down_val, t_down)
            k += 1
        return cmax_idx, down_sure
    
    def __get_init_down_first():
        cmin_idx, cmin = 0, low[0]
        cmax, up_sure = -_MAX, False
        up_pct, up_val, t_up = -_MAX, -_MAX, -_MAX
        k = 1
        while k < n and not up_sure:
            if low[k] < cmin:
                cmin_idx, cmin = k, low[k]
                cmax = -_MAX
            if high[k] >= cmax:
                cmax = high[k]
                up_pct, up_val = __cal_dif(cmin, cmax)
                t_up = k - cmin_idx
            up_sure = __up_sure(up_pct, up_val, t_up)
            k += 1
        return cmin_idx, up_sure
    
    def __get_init_ktype(zz):
        k_up, down_sure = __get_init_up_first()
        k_down, up_sure = __get_init_down_first()
        k_up0, k_down0 = k_up, k_down
        swift = True
        while (k_up == k_down) and (k_up < n) and (k_down < n):
            k_up_pre, k_down_pre = k_up, k_down
            if swift:
                k_up, _, _ = __confirm_low_from_ensure_high(k_up)
                k_down, _, _ = __confirm_high_from_ensure_low(k_down)
                swift = False
            else:
                k_up, _, _ = __confirm_high_from_ensure_low(k_up)
                k_down, _, _ = __confirm_low_from_ensure_high(k_down)
                swift = True
            if (k_up_pre == k_up) or (k_down_pre == k_down):
                break
            k_up_pre, k_down_pre = k_up, k_down
        if (down_sure and up_sure) or (not down_sure and not up_sure):
            if k_up <= k_down:
                k, ktype = k_up0, 1
            else:
                k, ktype = k_down0, -1
        else:
            if down_sure:
                k, ktype = k_up0, 1
            else:
                k, ktype = k_down0, -1
        zz[k] = ktype
        return k, ktype, zz
    
    # 找到最新一个确定转折点位置
    k = n - 1
    while k > 0 and zz[k] in [0, 5, -5]:
        k -= 1
    ktype = zz[k]
    if ktype in [1, -1]:
        zz = __update_zz_from_ensure(k, ktype, zz)
    else:
        k, ktype, zz = __get_init_ktype(zz)
        zz = __update_zz_from_ensure(k, ktype, zz)
    
    return _get_out2(high_, zz)
    
    
#%%
if __name__ == '__main__':
    import pandas as pd
    from dramkit.datsci import find_turns
    from dramkit import TimeRecoder, plot_series, load_csv
    from dramkit.datsci.find_turns import check_turns
    from finfactory.finplot.plot_candle import plot_candle
    
    def plot_candle_zz(data, zzcol='zigzag',
                       zz_high='high', zz_low='low',
                       **kwargs):
        '''在K线图上绘制ZigZag'''
        data = data.copy()
        data['col_zz1'] = data[zzcol].apply(lambda x: 1 if x > 0 else 0)
        data['col_zz-1'] = data[zzcol].apply(lambda x: 1 if x < 0 else 0)
        data['col_zz'] = data['col_zz1'] * data[zz_high] + \
                         data['col_zz-1'] * data[zz_low]
        data['col_zz'] = data[['col_zz1', 'col_zz-1', 'col_zz']].apply(
                         lambda x: x['col_zz'] if x['col_zz1'] == 1 or \
                                   x['col_zz-1'] == 1 else np.nan, axis=1)
        data['zz_loc'] = data['col_zz1'] + data['col_zz-1']
        if 'cols_to_label_info' in kwargs.keys():
            cols_to_label_info = kwargs['cols_to_label_info']
            del kwargs['cols_to_label_info']
            cols_to_label_info.update(
                {'col_zz': [['zz_loc', (1,), ('-b',), False]]})
        else:
            cols_to_label_info={'col_zz': [['zz_loc', (1,), ('-b',), False]]}
        if 'cols_other_upleft' in kwargs.keys():
            cols_other_upleft = kwargs['cols_other_upleft']
            del kwargs['cols_other_upleft']
            cols_other_upleft.update({'col_zz': ('.b', False)})
        else:
            cols_other_upleft = {'col_zz': ('.w', False)}
        plot_candle(data, cols_other_upleft=cols_other_upleft,
                    cols_to_label_info=cols_to_label_info,
                    **kwargs)
    
    
    tr = TimeRecoder()
    
    """
    # 二次曲线叠加正弦余弦
    N = 200
    t = np.linspace(0, 1, N)
    s = 6*t*t + np.cos(10*2*np.pi*t*t) + np.sin(6*2*np.pi*t)
    df = pd.DataFrame(s, columns=['test'])

    # t_min = None
    t_min = 5
    min_dif_val = 4
    t_max = 10
    df['label'] = find_turns(df['test'], t_min=t_min, t_max=t_max-1,
                             min_dif_val=min_dif_val)
    plot_series(df, {'test': ('.-k', None)},
                cols_to_label_info={
                    'test': [
                        ['label', (-1, 1), ('r^', 'gv'), None]
                        ]},
                figsize=(8, 3))
    kwargs = {'t_min_up': t_min, 't_min_down': t_min,
              't_max_up': t_max, 't_max_down': t_max,
              'val_min_up': min_dif_val, 'val_min_down': -min_dif_val,
              'pct_min_up': None, 'pct_min_down': None
              }
    
    high, low = df['test'], df['test']
    args = ()
    df['zigzag'] = find_zigzag(high, low, *args, **kwargs)
    df['zigzag'] = df['zigzag'].replace({5: 1, -5: -1})
    plot_series(df, {'test': ('.-k', None)},
                cols_to_label_info={
                    'test': [
                        ['zigzag', (-1, 1), ('r^', 'gv'), None]
                        ]},
                figsize=(8, 3))
    # """
    
    """
    # 测试：为什么没删除(33, 35), (73, 75)；为什么删除(45, 49), 79
    # 测试：为什么删除(26, 27)
    df = pd.DataFrame({'value': [
        97, -78, -18, -40, -27, -39, 55, 0, 35, -39, 43, 93, 9, -87, -88, -53, -97, -33,
        -7, 99, 86, 37, 43, 48, -91, -2, 55, -89, 48, 75, 97, 22, 8, -31, -24, 32, -54,
        -42, -81, 20, -71, -24, -56, -13, 18, 90, 45, 87, 59, -36, 14, 76, 95, -61, -47,
        41, -55, 5, -30, 69, 16, 89, 57, 23, -1, 49, -22, -7, -47, 99, 45, -55, 51, -35,
        12, 42, -90, -84, 53, 0]})
    
    t_min, t_max = 4, 20
    min_dif_val = 50
    max_dif_val = 80
    min_dif_pct = None
    max_dif_pct = None
    df['label'] = find_turns(df['value'],
                             t_min=t_min,
                             t_max=t_max,
                             min_dif_pct=min_dif_pct,
                             max_dif_pct=max_dif_pct,
                             min_dif_val=min_dif_val,
                             max_dif_val=max_dif_val,
                             plot_process=False,
                             plot_process_detail=False
                             )
    plot_series(df, {'value': ('.-k', None)},
                cols_to_label_info={
                    'value': [
                        ['label', (-1, 1), ('r^', 'gv'), None]
                        ]},
                figsize=(12, 7))
    OK, e = check_turns(df, df.columns[0], df.columns[1])
    if OK:
        print('极值点排列正确！')
    else:
        print('极值点排列错误:', e)
        
    kwargs = {'t_min_up': t_min, 't_min_down': t_min,
              't_max_up': t_max, 't_max_down': t_max,
              'val_min_up': min_dif_val, 'val_min_down': -min_dif_val,
              'val_max_up': max_dif_val, 'val_max_down': -max_dif_val
              }
    
    high, low = df['value'], df['value']
    args = ()
    df['zigzag'] = find_zigzag(high, low, *args, **kwargs)
    df['zigzag'] = df['zigzag'].replace({5: 1, -5: -1})
    plot_series(df, {'value': ('.-k', None)},
                cols_to_label_info={
                    'value': [
                        ['zigzag', (-1, 1), ('r^', 'gv'), None]
                        ]},
                figsize=(12, 7))
    # """


    # """
    fpath = '../_test/510050.SH_daily_qfq.csv'
    his_data = load_csv(fpath)
    his_data.rename(columns={'date': 'time'}, inplace=True)
    his_data.set_index('time', drop=False, inplace=True)

    # N = his_data.shape[0]
    N = 100
    data = his_data.iloc[-N:-1, :].copy()
    
    high, low = data['high'], data['low']
    kwargs = {'pct_min_up': 3/100,
              'pct_min_down': -3/100
              }
    args = ()
    data['zigzag'] = find_zigzag(high, low, *args, **kwargs)
    plot_candle_zz(data, zz_high='high', zz_low='low',
                   args_ma=None, args_boll=None, plot_below=None,
                   grid=False, figsize=(10, 6))
    # """


    """
    fpath = '../_test/zigzag_test2.csv'
    df = load_csv(fpath)
    df = df[['date', 'time', 'open', 'high', 'low', 'close', 'label']]
    dates = list(df['date'].unique())
    df = df[df['date'] == dates[0]].copy()
    plot_candle_zz(df, zzcol='label',
                   args_ma=None,
                   args_boll=None,
                   plot_below=None,
                   figsize=(10, 6),
                   tformat='%H:%M:%S')
    
    pct_min = -1/100
    # pct_min = None
    t_min = 15
    # t_min = None
    val_min = None
    kwargs = {'pct_min': pct_min,
              't_min': t_min,
              'val_min': val_min
              }    
    
    df['zigzag'] = find_zigzag(df['high'], df['low'], **kwargs)
    plot_candle_zz(df,
                    args_ma=None,
                    # args_boll=[15, 2],
                    args_boll=None,
                    plot_below=None,
                    figsize=(10, 6),
                    tformat='%H:%M:%S')
    
    # """
    
    tr.used()























