# -*- coding: utf-8 -*-
import logging
import uuid
from utils.utils import md5


def signatuer(*args, **kwargs):
    keys = sorted(kwargs.keys())
    key_str = "".join(keys)
    values_str = ""
    for key in keys:
        values_str += str(kwargs[key])
    logging.info("********Values_Str:{0}********".format(values_str))
    s = "{}{}".format(key_str, values_str)
    # 加密
    signature_str1 = md5(s)
    # 加盐加密na
    signature_str = md5("NCSS-SASH-{}".format(signature_str1))
    logging.info("********Sign_Str**********".format(signature_str))
    return signature_str


def token(*args, **kwargs):
    return uuid.uuid4().hex


if __name__ == '__main__':
    test = {}
    print signatuer(**test)
