# -*- coding: utf-8 -*-
# 路由列表
from handlers.api import LoginHandler,\
        TestHandler, LoginHtml, IndexHtml, \
        TestHtml,UploadFileHandler,GetWishListHandler,GetPrizeListHandler

urls = [(r"/html/v1/login/", LoginHtml),
        (r"/api/v1/login/", LoginHandler),
        (r"/api/v1/upload/", UploadFileHandler),
        (r"/api/v1/wish/list/", GetWishListHandler),
        (r"/api/v1/prize/list/", GetPrizeListHandler),
        (r"/", IndexHtml),
        (r"/html/v1/test/", TestHtml), ]
