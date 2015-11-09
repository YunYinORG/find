#!/usr/bin/env python
#coding=utf-8
import web
urls = (
    '/', 'index',
    '/verify', 'verify',
    '/broadcast','broadcast',
    '/weibo', 'weibo', #绑定weibo账号 
    '/log', 'log',
    '/code', 'code',
    '/phone', 'phone',
    '/test','test',
    '/hello','hello',
)


class test:
	def GET(self):
		return 'It works ! [test]';

if __name__ == "__main__":
	application = web.application(urls, globals()).run()
else :
	application = web.application(urls, globals()).wsgifunc()