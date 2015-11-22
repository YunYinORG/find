#!/usr/bin/env python
#coding=utf-8
import sys,os
reload(sys)
sys.setdefaultencoding( "utf-8" )
abspath = os.path.dirname(__file__)#兼容wsgi
sys.path.append(abspath)
if abspath:os.chdir(abspath)

import web

from controller.index import index
from controller.notify import notify,broadcast

import lib

web.config.debug = True
web.DEBUG=True
#url路由
urls = (
    '/', 'index',#首页
    '/notify/', 'notify',#通知
    '/notify/broadcast','broadcast',#广播
    '/weibo', 'weibo', #绑定weibo账号
    '/record', 'record',#查看记录
    '/phone', 'phone',#绑定手机
    '/phone/code', 'code',#手机验证码验证
    '/test','test',#可用性测试
)

class test:
    def GET(self):
        return "it works"

#启动服务
app = web.application(urls, globals())
if __name__ == "__main__":
    application = app.run()
else:
    application = app.wsgifunc()
