# -*- coding: utf-8 -*-
import tornado.websocket
import time
import tornado.web

class ClassName(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        username = self.get_cookie("username")
        self.write("<h1>username is %s</h1>" % username)


class View(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")


class Test(tornado.websocket.WebSocketHandler):
    # 接收消息初始化
    def open(self, *args, **kwargs):
        pass

    # print (self.request.remote_ip)
    # 接收到消息做什么
    def on_message(self, message):
        print ("----->服务器接收到消息")
        for i in range(0, 11):
            time.sleep(1)
            message = str(i)
            if i == 10:
                self.on_close()
            self.write_message(message)

    def allow_draft76(self):
        return True

    # def write_message(self, message, binary=False):
    #     for i in range(0,10):
    #         print ("------->服务器发送消息{index}".format(index=i))
    #         if i==10:
    #             self.on_close()
    def on_close(self):
        print ("---->轮询结束")

    def check_origin(self, origin):
        return True