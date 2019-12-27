# -*- coding: utf-8 -*-
import os
import random
import sqlite3
import zipfile

from utils.utils import Excel

PATH = r"H:\files"


class Template(object):
    def __init__(self):
        pass

    def __completion_note(self, *args, **kwargs):
        # 如果没有备注则补空，保证存入数据整齐
        split_group, = args
        if len(split_group) < 2:
            split_group.append("")
        return split_group

    def parsing_and_save_wishlist(self, *args, **kwargs):
        tmp_file_group, = args
        for tmp_file in tmp_file_group:
            with open(r'{}\{}'.format(PATH, tmp_file).decode('utf-8'), 'r') as f:
                lines = f.readlines()
                insert_group = [self.__completion_note(line.split('----')) for line in lines]
                self.save(insert_group)

    def save(self, *args, **kwargs):
        insert_group, = args
        sql = "INSERT INTO wish_list (gift_name,note)VALUES (?,?)"
        conn = sqlite3.connect('gift-box.db')
        cur = conn.cursor()
        cur.executemany(sql, tuple(insert_group))
        conn.commit()
        conn.close()

class WishBoxController(object):
    def __init__(self):
        pass

    def get_wish_list(self,*args,**kwargs):
        sql="SELECT * FROM wish_list"
        conn = sqlite3.connect('gift-box.db')
        cur = conn.cursor()
        cur.execute(sql)
        qs = cur.fetchall()
        conn.close()
        return qs

    def get_prize_list(self,*args,**kwargs):
        wish_list = self.get_wish_list()
        random.shuffle(wish_list)
        return random.sample(wish_list, len(wish_list)-1)

