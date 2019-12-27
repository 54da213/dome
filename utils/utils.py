# -*- coding: utf-8 -*-

import re
import random
import os
import logging
import xlrd
import requests
import json
import hashlib

from datetime import datetime
from xlwt import *
from xlrd import xldate_as_tuple


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

# 写入excel模块
class Excel(object):
    def __init__(self, write_file=None, read_file=None, encoding="utf-8", table_name="data"):
        self.write_file = write_file
        self.read_file = read_file
        self.encoding = encoding
        self.table_name = table_name
        self.file_p = None
        self.read_file_p = None
        if self.write_file:
            self.workbook = Workbook(self.encoding)
            self.file_p = self.workbook.add_sheet(self.table_name)
        if self.read_file:
            # 待开发 本次只需要写 所以读我就不写了 啦啦啦啦啦...
            self.read_file_p = xlrd.open_workbook(filename=self.read_file.decode(self.encoding))
            self.__sheet = self.read_file_p.sheet_by_index(0)
            self.__n = self.__sheet.nrows

    def get_rows_len(self):
        return self.__n

    # 写入文件
    def write(self, field_list, data_list):
        if not self.write_file:
            raise ValueError("Write_file can not be none")
        p = 0
        # 写入字段
        if field_list:
            if not isinstance(field_list, tuple):
                raise TypeError("Must be an iterable object")
            field_len = len(field_list)
            for i in range(field_len):
                self.file_p.write(0, i, field_list[i])

        # 写入内容
        # 可以根据传来的数据指针类型定制不同的写入策略
        # 这里只写了针对元祖列表
        if isinstance(data_list, list):
            rows = len(data_list)
            for r in range(p, rows):
                if (not isinstance(data_list[r], list)) and (not isinstance(data_list[r], tuple)):
                    raise TypeError("Must be an iterable object")
                cols = len(data_list[r])
                for c in range(cols):
                    # 写入excel
                    # 参数对应 行, 列, 值
                    self.file_p.write(r + 1, c, data_list[r][c])

    # 2019.12.12 新增读取
    def read_all(self, start_colx=0, end_colx=None):
        # 针对数据量少
        if not self.read_file_p:
            raise ValueError("read_file can not be none")
        data_group = []
        for i in xrange(self.get_rows_len()):
            row = []
            c =  len(self.__sheet.row_values(i))
            for j in xrange(c):
                value = self.__sheet.cell(i, j).value
                if self.__sheet.cell(i, j).ctype == 3:  # 类型为：3 是日期格式
                    date = xldate_as_tuple(value,0)
                    v = str(datetime(*date))
                else:
                    v = self.__sheet.cell(i, j).value
                row.append(v)
                data_group.append(v)
        #
        #
        return data_group

    def read_row(self, row=0, start_colx=0, end_colx=None):
        if not self.read_file_p:
            raise ValueError("read_file can not be none")
        if self.get_rows_len() == 0:
            return []
        return self.__sheet.row_values(rowx=row, start_colx=start_colx, end_colx=end_colx)

    def save(self):
        self.workbook.save(self.write_file)


def word_process(word):
    return word.strip()


class FileController(object):
    def upload(self, *args, **kwargs):
        path, file_metas = args
        file_name_group=[]
        for meta in file_metas:
            filename = meta['filename']
            file_name_group.append(filename)
            file_path = os.path.join(path, filename)

            with open(file_path.decode('utf-8'), 'wb') as up:
                up.write(meta['body'])
        return file_name_group


