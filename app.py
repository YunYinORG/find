#!/usr/bin/env python
#coding=utf-8
import sys,os
abspath = os.path.dirname(__file__)#兼容wsgi
sys.path.append(abspath)
if abspath:os.chdir(abspath)
import web
from controller.index import index

#url路由
urls = (
    '/', 'index',
    '/verify', 'verify',
    '/broadcast','broadcast',
    '/weibo', 'weibo', #绑定weibo账号
    '/log', 'log',
    '/code', 'code',
    '/phone', 'phone',
    '/test','test',
)

#测试
class test:
	def GET(self):
		return 'It works ! [test]';

#启动服务
app = web.application(urls, globals())
if __name__ == "__main__":
	application = app.run()
else :
    application = app.wsgifunc()