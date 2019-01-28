# -*- coding: utf-8 -*-

import random, string
import hashlib
from bs4 import BeautifulSoup
import re
import uuid
import re
import json
import requests


# 数据处理

class WebCrawler(object):
    def __init__(self):
        self.headers={}

    def get_html(self):
        pass

    def get_urls(self,page_url):
        return []

    def get_all_urls(self):
        return []

class Word(object):
    pass


def app():
    wc = WebCrawler()
    #获取所有页的
    all_urls = wc.get_all_urls()
    for page_url in all_urls:
        urls = wc.get_urls(page_url)
        for url in urls:
            html = wc.get_html()
            soup = BeautifulSoup(html, "html5lib")

if __name__ == '__main__':
    app()
