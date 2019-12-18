# -*- coding: utf-8 -*-
import functools
import json
from tornado import gen
import tornado.options
from log import *
from torndsession.sessionhandler import SessionBaseHandler
from signature import signatuer


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
        if METHOD == "GET":
            param = {k: v[0] for k, v in self.request.arguments.items() if v}
        elif METHOD == "POST":
            param = self.get_body_arguments()

        local_signatuer_str = signatuer(**param)
        headers = self.request.headers
        user_signatuer_str = headers["signatuer"]
        if local_signatuer_str != user_signatuer_str:
            return
        token = headers.get("token")
        if (not token) and ("/api/v1/login/" not in self.request.uri):
            return
        if "/api/v1/login/" in self.request.uri:
            return "success"
        return self.get_session(token)

    # def write_error(self, status_code, **kwargs):
    #     if status_code==400:
    #
    #     self.write("Gosh darnit, user! You caused a %d error." % status_code)
