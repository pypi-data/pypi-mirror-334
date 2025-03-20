import backtrader as bt
import os
import pytz
from datetime import datetime, timedelta, timezone
from ffquant.utils.Logger import stdout_log
from ffquant.indicators.ActBuySellHedgePos import ActBuySellHedgePos

__ALL__ = ['PricePattern']

class PricePattern(ActBuySellHedgePos):
    params = (
        ('url', os.getenv('INDEX_COLLECT_LIST_URL', default='http://192.168.25.127:8285/index/collect/list')),
        ('symbol', 'PV_MONITOR:HSI1'),
        ('timeframe', bt.TimeFrame.Seconds),
        ('compression', 30),
    )

    lines = (
        'close',
        'turnover',
        'premium',
    )

    # 子类需要实现这个方法 决定最后返回给backtrader框架的indicator结果
    def determine_final_result(self):
        self.lines.close[0] = float('-inf')
        self.lines.turnover[0] = float('-inf')
        self.lines.premium[0] = float('-inf')

        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        if current_bar_time_str in self.cache:
            result = self.cache[current_bar_time_str]

            for key, value in dict(result).items():
                if key == 'openTime' or key == 'closeTime':
                    continue

                if key == 'close' or key == 'turnover' or key == 'premium':
                    line = getattr(self.lines, key)
                    line[0] = float(value)
            return result['closeTime']
        else:
            return 0

    def prepare_params(self, start_time_str, end_time_str):
        params = {
            'symbol': self.p.symbol,
            'interval': '30S',
            'startTime' : start_time_str,
            'endTime' : end_time_str
        }

        return params