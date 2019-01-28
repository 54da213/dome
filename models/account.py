# -*- coding: utf-8 -*-
import abc
import re
import uuid as uid
import logging
import random
import hashlib
import base64

import torndb
from config import HOST, USER, PWD, DATABASE_NAME,CHECKCODE_N,ENCRYPT_STR


class AccountBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, user):
        self.user = user

    @abc.abstractmethod
    def login_tel(self,pwd):
        pass

    @abc.abstractmethod
    def log_in_wc(self):
        pass

    @abc.abstractmethod
    def log_out(self):
        pass

    @abc.abstractmethod
    def update_pwd(self,new_pwd):
        pass

    @abc.abstractmethod
    def check(self,pwd):
        pass

#用户模型
class Account(AccountBase):
    def __init__(self, user=None):
        super(Account, self).__init__(user)
        self.row = None
        if self.user:
            sql = "SELECT * FROM account WHERE user = %s"
            db = torndb.Connection(host=HOST, database=DATABASE_NAME, user=USER, password=PWD)
            row = db.get(sql, self.user)
            if row:
                self.row = row
    #手机
    def login_tel(self,pwd):
        msg  = self.check(pwd)
        if msg:
            return msg
    #微信
    def log_in_wc(self):
        pass


    def log_out(self):
        pass


    def update_pwd(self,new_pwd):
        if not self.row:
            logging.exception("账户修改异常")
            raise RuntimeError("账户修改异常")
        sql="UPDATE account SET pwd=%s WHERE user=%s;"
        db = torndb.Connection(host=HOST, database=DATABASE_NAME, user=USER, password=PWD)
        count = db.execute_rowcount(sql,new_pwd,self.row["user"])
        if count!=1:
            return "修改失败"

    def check(self,pwd):
        pwd="{0}{1}".format(pwd,ENCRYPT_STR)
        encrypt = Encrypt(encrypt_word=pwd)
        if self.row["pwd"]!=encrypt.encrypt():
            return "密码错误"


#验证码模型
class VerificationCode(object):
    def __init__(self, tel):
        self.check_code = ""
        self.tel = tel

    def code(self):
        # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
        self.check_code = ''.join(str(i) for i in random.sample(range(0, 9), CHECKCODE_N))

    def send_code(self):
        pass

    # 写入数据库记录
    def save(self):
        db = torndb.Connection(host=HOST, database=DATABASE_NAME, user=USER, password=PWD)
        # 保存时先检查一下用户是否已经存在 如果存在更新验证码即可
        '''
        这是因为有时成功发送了验证码但是用户没有收到  一分钟以后再次发送
        '''
        sql = "SELECT * FROM account WHERE user = %s"
        row = db.query(sql, self.tel)
        if row:
            sql = "UPDATE account SET code=%s WHERE user=%s;"
            count = db.execute_rowcount(sql, self.check_code, self.tel)
            if count != 1:
                msg = "再次请求更改验证码错误"
                raise RuntimeError(msg)
            return

        pwd = ""
        sql = "INSERT INTO account (user,pwd,code,nick_name)VALUES(%s,%s,%s,%s);"
        # 生成一个昵称
        nick_name = str(uid.uuid4())[0:6]
        count = db.execute_rowcount(sql, self.tel, pwd, self.check_code, nick_name)
        if count != 1:
            msg = "验证码保存失败"
            raise RuntimeError(msg)

    def check(self, code):
        sql = "SELECT code FROM account WHERE user = %s"
        db = torndb.Connection(host=HOST, database=DATABASE_NAME, user=USER, password=PWD)
        row=db.get(sql,self.tel)
        if row["code"] != code:
            return "验证码错误"

#加密模型
class Encrypt(object):
    def __init__(self,encrypt_word=None):
        self.encrypt_word=encrypt_word
    def encrypt(self):
        hl = hashlib.md5()
        hl.update(self.encrypt_word.encode(encoding='utf-8'))
        return  hl.hexdigest()

#Token模型
class Token(object):
    def __init__(self):
        pass
