# -*- coding: utf-8 -*-
import functools
import json
from tornado import gen
import tornado.options
from log import *
from torndsession.sessionhandler import SessionBaseHandler
from signature import signatuer

AUTH_SUCCESS = "AuthenticationSuccessful"


# 权限验证的装饰器
def superuser_only(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        superright = self.get_session("superright") == "1"
        if not superright:
            self.write_error(403)
            return
        return method(self, *args, **kwargs)

    return wrapper


class BaseHandler(SessionBaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        def __init__(self, application, request, **kwargs):
            super(BaseHandler, self).__init__(application, request, **kwargs)

    def write_resp200(self, response, err_code=0, _err=''):
        self.set_header('Content-type', 'application/json')
        _response = {
            "err_code": err_code,
            "data": response,
            "err_msg": _err
        }
        self.write(json.dumps(_response))
        self.finish()

    def write_resp400(self, _err, response="", err_code=400):
        self.set_header('Content-type', 'application/json')
        _response = {
            "data": response,
            "err_code": err_code,
            "err_msg": _err
        }
        self.write(json.dumps(_response))
        self.finish()

    def write_resp500(self, response, err_code=500, _err=''):
        self.set_header('Content-type', 'application/json')
        _response = {
            "err_code": err_code,
            "data": response,
            "err_msg": _err
        }
        self.write(json.dumps(_response))
        self.finish()

    def json(self):
        return json.loads(self.request.body)

    def get_session(self, key):
        return self.session.get(key)

    # 验证登录状态
    def get_current_user(self):
        METHOD = self.request.method
        headers = self.request.headers
        # 登录页面
        if self.request.uri.startswith("/html/v1/login/"):
            return AUTH_SUCCESS
        # 登录接口
        if self.request.uri == "/api/v1/login/":
            param = json.loads(self.request.body)
            local_sign = signatuer(**param)
            user_sign = headers["signatuer"]
            if local_sign == user_sign:
                return AUTH_SUCCESS
        if self.request.uri.startswith("/?token") or self.request.uri.startswith("/html"):
            token = self.get_argument("token")
            return self.get_session(token)
        # API
        if self.request.uri.startswith("/api"):
            token = headers.get("Token")
            if not self.get_session(token):
                return
            if METHOD == "GET":
                param = {k: v[0] for k, v in self.request.arguments.items() if v}
            elif METHOD == "POST":
                if self.request.uri == "/api/v1/upload/":
                    param = json.loads(self.get_arguments("data")[0])
                else:
                    param = self.json()
            local_sign = signatuer(**param)
            user_sign = headers["signatuer"]
            if local_sign != user_sign:
                return
            return AUTH_SUCCESS

    # def write_error(self, status_code, **kwargs):
    #     if status_code==400:
    #
    #     self.write("Gosh darnit, user! You caused a %d error." % status_code)
