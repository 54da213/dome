# -*- coding: utf-8 -*-

import re
import requests
import json


# 数据处理
class DataHandle(object):
    @staticmethod
    def match(data):
        return re.findall('\((.*?)\)', data)
    @staticmethod
    def to_json(data):
        return json.loads(data)