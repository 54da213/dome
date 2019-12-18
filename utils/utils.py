# -*- coding: utf-8 -*-

import re
import logging
import requests
import json
import hashlib


def md5(_str):
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(_str.encode(encoding='utf-8'))
    logging.info('**********MD5加密前为:{}************'.format(_str))
    logging.info('**********MD5加密后为:{}'.format(hl.hexdigest()))
    return hl.hexdigest()


def word_process(word):
    return word.strip()
