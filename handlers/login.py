# -*- coding: utf-8 -*-
import logging
import re
import uuid

from tornado import gen
from tornado.web import authenticated

from base import BaseHandler
from models.account import Account, VerificationCode, Encrypt
from config import ENCRYPT_STR


# 登陆
class LoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        user = self.get_argument("tel")
        pwd = self.get_argument("pwd", None)
        _type = self.get_argument("type")

        if not (user and _type):
            return self.write_resp400("传入参数不完整")

        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', user):
            return self.write_resp400("电话格式错误")
        account = None
        try:
            account = Account(user)
        except Exception as e:
            self.write_resp400("该用户不存在")
        msg = ""
        # 手机登陆
        if _type == "0":
            msg = account.login_tel(pwd)
        # 微信登陆
        elif _type == "1":
            msg = account.log_in_wc()
        else:
            self.write_resp400("参数错误")
        if msg:
            self.write_resp400(msg)
        # 跳转
        token = str(uuid.uuid4())
        self.session[token] = account.user
        self.write_resp200(token)


class LogOutHandler(BaseHandler):
    def post(self, *args, **kwargs):
        token = self.get_argument("token")
        try:
            self.session.delete(token)
        except Exception as e:
            logging.exception(e)
            self.write_resp500("退出失败")

        self.write_resp200({})


# post 获取验证码
class EnrollmentHandler(BaseHandler):
    def post(self, *args, **kwargs):
        data = self.json()
        tel = data["tel"]
        if not tel:
            return self.write_resp400("传入参数不完整")
        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', tel):
            return self.write_resp400("电话格式错误")
        vcc = VerificationCode(tel)
        vcc.code()
        try:
            msg = vcc.save()
        except Exception as e:
            logging.exception(e)
            return self.write_resp500("验证码获取异常")
        if msg:
            return self.write_resp400(msg)
        try:
            vcc.send_code()
        except Exception as e:
            logging.info(str(e))
            return self.write_resp400("验证码发送异常")

        return self.write_resp200(vcc.check_code)

    def get(self, *args, **kwargs):
        tel = self.get_argument("tel")
        if not tel:
            return self.write_resp400("传入参数不完整")
        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', tel):
            return self.write_resp400("电话格式错误")
        code = self.get_argument("code")
        vcc = VerificationCode(tel)
        try:
            msg = vcc.check(code)
        except Exception as e:
            return self.write_resp400("电话号码错误")
        if msg:
            self.write_resp400(msg)
        # 生成一个token
        token = str(uuid.uuid4())
        return self.write_resp200(token)


# 更改账户密码
class UpdatePwd(BaseHandler):
    def post(self, *args, **kwargs):
        data = self.json()
        tel = data.get("tel")
        code = data.get("code")
        pwd = data.get("pwd")
        if not (tel and code and pwd):
            return self.write_resp400("传入参数不完整")

        if not re.match(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$', tel):
            return self.write_resp400("电话格式错误")
        vcc = VerificationCode(tel)
        try:
            msg = vcc.check(code)
        except Exception as e:
            return self.write_resp400("电话号码错误")
        if msg:
            return self.write_resp400(msg)
        account = Account(user=tel)
        try:
            high_level_pwd = "{0}{1}".format(pwd, ENCRYPT_STR)
            encrypt = Encrypt(high_level_pwd)
            msg = account.update_pwd(encrypt.encrypt())
        except Exception as e:
            logging.info(e)
            return self.write_resp500("修改异常")
        if msg:
            return self.write_resp400(msg)
        return self.write_resp200({})
