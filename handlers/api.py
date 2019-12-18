# -*- coding: utf-8 -*-
import logging
import tornado
from handlers.base import BaseHandler

from handlers.user import User

ErrMsg = "错误,请联系管理员"


class LoginHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        account = self.get_argument("account")
        pwd = self.get_argument("pwd")
        user = User()
        try:
            token = user.login(account, pwd)
        except Exception as e:
            logging.error("------登录异常:{}-------".format(e.message))
            self.write_resp400(ErrMsg)
        if not token:
            return self.write_resp400(user.login_err_msg)
        self.session[token] = {"account": account}
        return self.write_resp200(token)


class TestHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        print self.current_user["account"]
        return self.write_resp200("")
