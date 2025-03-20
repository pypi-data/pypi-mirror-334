import backtrader as bt
import os
import pytz
import requests
from datetime import datetime, timedelta, timezone
import time
from ffquant.utils.Logger import stdout_log

__ALL__ = ['ProdBuySellSeqZyj']

class ProdBuySellSeqZyj(bt.Indicator):
    params = (
        ('url', os.getenv('INDEX_LIST_URL', default='http://192.168.25.127:8285/index/list')),
        ('symbol', 'CAPITALCOM:HK50'),
        ('max_retries', 15),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1),
        ('test', None),
        ('debug', None),
    )

    lines = (
        "futureSeq",
        "bearSeq",
        "zyjMinMaxDiffChange",
        "zyjMinMaxDiff",
        "futureZyj",
        "etf",
        "bullZyj",
        "closeTime",
        "indexSeq",
        "bear",
        "lvetfSeq",
        "openTime",
        "stock",
        "stockZyj",
        "cnetfSeq",
        "etfZyj",
        "bullSeq",
        "stockSeq",
        "etfSeq",
        "lvetf",
        "indx",
        "cnetf",
        "indexZyj",
        "cnetfZyj",
        "lvetfZyj",
        "future",
        "bull",
        "bearZyj",
    )

    TEST = False
    DEBUG = False

    def __init__(self):
        super().__init__()
        if self.p.test is None:
            self.p.test = self.TEST

        if self.p.debug is None:
            self.p.debug = self.DEBUG

        self.cache = {}

    # 根节点的openTime和closeTime表示属于哪根K线，子节点的openTime和closeTime表示信号的原材料的时间
    def handle_api_resp(self, result):
        result_time_str = datetime.fromtimestamp(result['closeTime'] / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
        self.cache[result_time_str] = result

    # 子类需要实现这个方法 决定最后返回给backtrader框架的indicator结果
    def determine_final_result(self):
        self.lines.futureSeq[0] = float('-inf')
        self.lines.bearSeq[0] = float('-inf')
        self.lines.zyjMinMaxDiffChange[0] = float('-inf')
        self.lines.zyjMinMaxDiff[0] = float('-inf')
        self.lines.futureZyj[0] = float('-inf')
        self.lines.etf[0] = float('-inf')
        self.lines.bullZyj[0] = float('-inf')
        self.lines.closeTime[0] = float('-inf')
        self.lines.indexSeq[0] = float('-inf')
        self.lines.bear[0] = float('-inf')
        self.lines.lvetfSeq[0] = float('-inf')
        self.lines.openTime[0] = float('-inf')
        self.lines.stock[0] = float('-inf')
        self.lines.stockZyj[0] = float('-inf')
        self.lines.cnetfSeq[0] = float('-inf')
        self.lines.etfZyj[0] = float('-inf')
        self.lines.bullSeq[0] = float('-inf')
        self.lines.stockSeq[0] = float('-inf')
        self.lines.etfSeq[0] = float('-inf')
        self.lines.lvetf[0] = float('-inf')
        self.lines.indx[0] = float('-inf')
        self.lines.cnetf[0] = float('-inf')
        self.lines.indexZyj[0] = float('-inf')
        self.lines.cnetfZyj[0] = float('-inf')
        self.lines.lvetfZyj[0] = float('-inf')
        self.lines.future[0] = float('-inf')
        self.lines.bull[0] = float('-inf')
        self.lines.bearZyj[0] = float('-inf')

        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        if current_bar_time_str in self.cache:
            result = self.cache[current_bar_time_str]

            for key, value in dict(result).items():
                if key == 'openTime' or key == 'closeTime':
                    continue

                if str(key).endswith('Seq') or str(key).endswith('Zyj') or str(key).endswith('Diff') or str(key).endswith('DiffChange'):
                    line = getattr(self.lines, key)
                    line[0] = float(value)
                elif str(value) != '':
                    if key == 'index':
                        key = 'indx'
                    line = getattr(self.lines, key)
                    if str(value) == 'B':
                        line[0] == 1
                    elif str(value) == 'S':
                        line[0] == -1
            return result['closeTime']
        else:
            return 0

    def next(self):
        super().next()
        cur_bar_local_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        cur_bar_local_time_str = cur_bar_local_time.strftime('%Y-%m-%d %H:%M:%S')

        # 实时模式
        is_live = self.data.islive()
        if is_live:
            # 如果不在缓存中 则请求数据
            if cur_bar_local_time_str not in self.cache:
                start_time = cur_bar_local_time - timedelta(minutes=self.p.compression)
                end_time = cur_bar_local_time
                self.batch_fetch(start_time, end_time)
            else:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, current_time_str: {cur_bar_local_time_str}, hit cache: {self.cache[cur_bar_local_time_str]}")
        else:
            # 非实时模式 一次性把所有的数据都捞回来
            if len(self.cache) == 0:
                start_time_str = self.data.p.start_time
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
                end_time_str = self.data.p.end_time
                end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

                self.batch_fetch(start_time, end_time)
            
            if cur_bar_local_time_str not in self.cache:
                start_time = cur_bar_local_time - timedelta(minutes=self.p.compression)
                end_time = cur_bar_local_time
                self.batch_fetch(start_time, end_time)
            
            if cur_bar_local_time_str in self.cache:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, current_time_str: {cur_bar_local_time_str}, hit cache: {self.cache[cur_bar_local_time_str]}")

        # 不管是实时模式还是非实时模式 都在此判断最终应该返回什么数值
        create_time = self.determine_final_result()

        # Replace -info with previous value. Starting value is zero. heartbeat info print
        for line_name in self.lines.getlinealiases():
            line = getattr(self.lines, line_name)
            if line[0] == float('-inf'):
                if len(self) > 1:
                    stdout_log(f"[CRITICAL], {self.__class__.__name__}, kline time: {cur_bar_local_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')}, line[0] inherited from line[-1]: {line[-1]}")
                    line[0] = line[-1]

            kline_local_time_str = cur_bar_local_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')
            create_local_time_str = datetime.fromtimestamp(create_time / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')

            # 这里的打印最终会输出到标准输出日志中 这样的日志被用于分析行情的延迟等问题
            stdout_log(f"[INFO], {self.__class__.__name__}, kline time: {kline_local_time_str}, create_time: {create_local_time_str}, {line_name}: {line[0]}")

    def prepare_params(self, start_time_str, end_time_str):
        params = {
            'symbol': self.p.symbol,
            'type': 'index_zyj',
            'key_list': 'prod_bs_seq_zyj',
            'startTime' : start_time_str,
            'endTime' : end_time_str
        }

        return params

    def batch_fetch(self, start_time: datetime, end_time: datetime):
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        params = self.prepare_params(start_time_str, end_time_str)

        # fill with -inf
        # interval = 60 * self.p.compression
        # cur_time = start_time
        # while cur_time < end_time:
        #     # HTTP请求是open标记法 cache的key是close标记法 所以需要先递增cur_time
        #     cur_time = cur_time + timedelta(seconds=interval)
        #     self.cache[cur_time.strftime('%Y-%m-%d %H:%M:%S')] = {'value': float('-inf'), 'create_time': 0, 'raw_material_time': 0}

        retry_count = 0
        max_retry_count = self.p.max_retries
        while retry_count < max_retry_count:
            retry_count += 1
            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, fetch data params: {params}, url: {self.p.url}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, fetch data response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

            if response.get('results') is not None and len(response['results']) > 0:
                results = response['results']
                results.sort(key=lambda x: x['closeTime'])
                for result in results:
                    self.handle_api_resp(result)
                break
            time.sleep(1)