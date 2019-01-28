# -*- coding: utf-8 -*-
# 路由列表
from handlers.login import EnrollmentHandler,LoginHandler,UpdatePwd
from handlers.market import GetMarketNumHandler,GetMarketGainHandler,ProportionHandler,GetRmdListHandler,StockQuotesHandler
urls = [(r"/api/v1/login/PIN/", EnrollmentHandler),
        (r"/api/v1/login/", LoginHandler),
        (r"/api/v1/user/update/pwd/", UpdatePwd),
        (r"/api/v1/market/values/", GetMarketNumHandler),
        (r"/api/v1/market/gain/", GetMarketGainHandler),
        (r"/api/v1/market/proportion/", ProportionHandler),
        (r"/api/v1/market/recommend/list/", GetRmdListHandler),
        (r"/api/v1/market/quotation/list/", StockQuotesHandler)]
