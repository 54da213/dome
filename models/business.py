# -*- coding: utf-8 -*-
import logging

from tornado.web import asynchronous
from tornado.gen import engine, Task
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from utils.utils import DataHandle


# 大盘策略

class MarketStrategy(object):
    # 获取 上 深  创 基本信息
    @asynchronous
    @engine
    def last(self):
        '''
        数据来自同花顺
        '''
        url = "http://d.10jqka.com.cn/v6/time/hs_399006/last.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            "Referer": "http://q.10jqka.com.cn/",
            "Cookie": "log=; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1540708038,1540821052; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1540821055; v=Aubi4lU5gaYiblUCE1azdf9QN1drxyqK_Ate5dCP0onkU4jBOFd6kcybrv-j",
            "Host": "d.10jqka.com.cn"}
        r = HTTPRequest(method="GET", url=url, headers=headers)
        client = AsyncHTTPClient()
        response = yield Task(client.fetch, r)
        raise response.code
        # 创业
