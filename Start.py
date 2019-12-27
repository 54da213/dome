# -*- coding: utf-8 -*-
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.websocket
import os
from tornado.options import define, options

from config import BASE_DIR,SESSION_LIFETIME

from urls import urls


define("port", type=int, default=9000)


configs = dict(
    template_path=os.path.join(BASE_DIR, "templates"),
    static_path=os.path.join(BASE_DIR, "static"),
    login_url="/html/v1/login/",
)


class CustomApplication(tornado.web.Application):
    def __init__(self, urls, configs):
        handlers = urls
        settings = configs
        session_settings = dict(
            driver="file",
            driver_settings=dict(
                host="#_sessions",
            ),
            sid_name='sessionID',
            session_lifetime=SESSION_LIFETIME,
            force_persistence=True,
        )
        settings.update(session=session_settings)
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


def create_app():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(CustomApplication(urls, configs))
    # 调用端口
    http_server.listen(options.port)
    # 启动监听
    tornado.ioloop.IOLoop.instance().start()


app = create_app()

if __name__ == "__main__":
    app()
