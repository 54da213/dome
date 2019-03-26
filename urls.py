# -*- coding: utf-8 -*-
# 路由列表
from handlers.login import EnrollmentHandler,LoginHandler,UpdatePwd
from handlers.api.test import Test,GetCarList
urls = [(r"/api/v1/login/PIN/", EnrollmentHandler),
        (r"/api/v1/login/", LoginHandler),
        (r"/api/v1/test/", Test),
        (r"/api/v1/car/list", GetCarList)]
