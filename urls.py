# -*- coding: utf-8 -*-
# 路由列表
from handlers.api import LoginHandler,TestHandler
urls = [(r"/api/v1/login/", LoginHandler),
        (r"/api/v1/test/", TestHandler),]
