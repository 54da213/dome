# -*- coding: utf-8 -*-
import logging
import tornado
import json
from handlers.base import BaseHandler

from handlers.user import User
from handlers.PrizePool import Template, WishBoxController
from utils.utils import FileController

ErrMsg = "错误,请联系管理员"
Warning = "传入参数不完整"


class LoginHtml(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        try:
            self.render("index.html")
        except Exception as e:
            return self.write_resp400(e.message)


class IndexHtml(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        try:
            token = self.get_argument("token")
            self.render("admin.html", **{"token": token})
        except Exception as e:
            return self.write_resp400(e.message)


class TestHtml(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        token = self.get_argument("token")
        try:
            self.render("test.html",**{"token": token})
        except Exception as e:
            return self.write_resp400(e.message)


class LoginHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        account = data.get("account")
        pwd = data.get("pwd")
        user = User()
        try:
            token = user.login(account, pwd)
        except Exception as e:
            logging.error("------登录异常:{}-------".format(e.message))
            self.write_resp400(ErrMsg)
        if not token:
            return self.write_resp400(user.login_err_msg)
        self.session[token] = {"account": account}
        self.set_cookie("token", token)
        return self.write_resp200(token)


class UploadFileHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        file_metas = self.request.files.get("file")
        fc = FileController()
        try:
            tmp_file_group = fc.upload(r"H:\files", file_metas)
        except Exception as e:
            logging.error("----配置模板上传异常:{}----", e.message)
            return self.write_resp400(ErrMsg)

        tmp = Template()
        try:
            tmp.parsing_and_save_wishlist(tmp_file_group)
        except Exception as e:
            logging.error("----配置模板解析异常:{}----".format(e.message))
            return self.write_resp400(ErrMsg)
        return self.write_resp200("")


class GetWishListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        wish = WishBoxController()
        try:
            qs = wish.get_wish_list()
        except Exception as e:
            logging.error(e.message)
            return self.write_resp400(ErrMsg)
        return self.write_resp200(qs)


class GetPrizeListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        wish = WishBoxController()
        try:
            qs = wish.get_prize_list()
        except Exception as e:
            logging.error(e.message)
            return self.write_resp400(ErrMsg)
        return self.write_resp200(qs)


class TestHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self):
        self.render("admin.html")
