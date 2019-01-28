# -*- coding: utf-8 -*-
import logging
import json
import random

import html5lib
from bs4 import BeautifulSoupssddd

from tornado.web import asynchronous
from tornado.gen import engine, Task, coroutine

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from base import BaseHandler
from utils.utils import DataHandle
from models.business import MarketStrategy


class GetMarketNumHandler(BaseHandler):
    @coroutine
    def get(self, *args, **kwargs):
        url = "http://api.money.126.net/data/feed/0000001,1399001,1399006,money.api"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            "Referer": "http://quotes.money.163.com/0000001.html"}
        r = HTTPRequest(method="GET", url=url, headers=headers)
        client = AsyncHTTPClient()
        response = yield Task(client.fetch, r)
        if response.code != 200:
            self.write_resp200("获取数据失败 %s" % (response.code))
            return
        try:
            data = DataHandle.to_json(DataHandle.match(response.body)[0])
        except Exception as e:
            logging.info(e)
            self.write_resp200("")
            return
        self.write_resp200(data)

class GetMarketGainHandler(BaseHandler):
    @coroutine
    def get(self, *args, **kwargs):
        url = "http://q.10jqka.com.cn/api.php?t=indexflash&"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            "Referer": "http://q.10jqka.com.cn/",
            "Host": "q.10jqka.com.cn",
            "Cookie": "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1540708038,1540821052; v=ApyYhDMLK3MrON-vfT7pe_EibbFNFUA_wrlUA3adqAdqwTLnniUQzxLJJJHF",
            "Connection": "keep-alive"}
        r = HTTPRequest(method="GET", url=url, headers=headers)
        client = AsyncHTTPClient()
        response = yield Task(client.fetch, r)
        if response.code != 200:
            self.write_resp200("获取数据失败 %s" % (response.code))
            return
        try:
            data = json.loads(response.body)
            t = (data["zdfb_data"]["znum"], data["zdfb_data"]["dnum"], data["zdt_data"]["last_zdt"]["ztzs"],
                 data["zdt_data"]["last_zdt"]["dtzs"])
            self.write_resp200(t)
        except Exception as e:
            logging.info(e)
            self.write_resp200("获取数据失败 %s" % (response.code))
            return


# 最优仓位比例 (后改大盘评级)
class ProportionHandler(BaseHandler):
    @coroutine
    def get(self, *args, **kwargs):
        cash = random.randint(10, 15)
        weights = random.randint(45, 65)
        medium = 100 - (cash + weights)
        self.write_resp200((cash, weights, medium))


# 推荐列表
class GetRmdListHandler(BaseHandler):
    @coroutine
    def get(self, *args, **kwargs):
        url = "http://data.10jqka.com.cn/rank/lxsz/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            "Referer": "http://data.10jqka.com.cn/rank/cxg/",
            "Host": "data.10jqka.com.cn",
            "Cookie": "Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1541317164,1542033640;"
                      "Hm_lvt_f79b64788a4e377c608617fba4c736e2=1541317164,1542033640;"
                      "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1540708038,1540821052,1541317164,1542033640;"
                      "Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1542033664;"
                      "Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1542033664;"
                      "Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1542033664;"
                      "v=AjQwzJvz047GV0dC7_3BIxm6BfmlDVuCmjDsJM6VxDBC2dov9h0oh-pBvNkd",
            "Connection": "keep-alive"}
        r = HTTPRequest(method="GET", url=url, headers=headers)
        client = AsyncHTTPClient()
        response = yield Task(client.fetch, r)
        # print response.body
        if response.code != 200:
            self.write_resp200("获取数据失败 %s" % (response.code))
            return
        html = response.body
        soup = BeautifulSoup(html, "html5lib")
        attrs = {"class": "m-table J-ajax-table"}
        values = []
        fields = []
        try:
            # print soup.find_all(name='table',attrs=attrs).select('tbody')
            ths = soup.select('table[class="m-table J-ajax-table"] thead tr th')
            for th in ths:
                a = th.select('.J-ajax-a')
                fields.append(a[0].get_text()) if a else fields.append(th.string)
            trs = soup.select('table[class="m-table J-ajax-table"] tbody tr')
            for tr in trs:
                tds = tr.select('td')
                rows = [td.string for td in tds]
                values.append(rows)
        except Exception as e:
            logging.info(e.message)
        resp = {"fields": fields, "values": values}
        self.write_resp200(resp)


# 个股行情
class StockQuotesHandler(BaseHandler):
    @coroutine
    def get(self):
        url = "http://q.10jqka.com.cn/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = HTTPRequest(method="GET", url=url, headers=headers)
        client = AsyncHTTPClient()
        response = yield Task(client.fetch, r)
        # print response.body
        if response.code != 200:
            self.write_resp200("获取数据失败 %s" % (response.code))
            return
        html = response.body
        soup=BeautifulSoup(html,"html5lib")
        fields=[]
        values=[]
        try:
            ths = soup.select('table[class="m-table m-pager-table"] thead tr th')
            for th in ths:
                a = th.select('a[field]')
                fields.append(a[0].get_text()) if a else fields.append(th.string)
            trs = soup.select('table[class="m-table m-pager-table"] tbody tr')
            for tr in trs:
                tds = tr.select('td')
                rows = [td.string for td in tds]
                values.append(rows)
        except Exception as e:
            logging.info(e.message)
        resp={"fields":fields,"values":values}
        self.write_resp200(resp)

#大盘评级
class GetInvestRateHandler(BaseHandler):
    def get(self, *args, **kwargs):
        url = "http://q.10jqka.com.cn/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = HTTPRequest(method="GET", url=url, headers=headers)
        client = AsyncHTTPClient()
        response = yield Task(client.fetch, r)
        # print response.body
        if response.code != 200:
            self.write_resp200("获取数据失败 %s" % (response.code))
            return
        html = response.body




