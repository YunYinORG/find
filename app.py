#!/usr/bin/env python
#coding=utf-8
import web
import urllib2
import urllib
urls = (
    '/', 'index',
    '/verify', 'verify',
    '/broadcast','broadcast',
    '/weibo', 'weibo', #绑定weibo账号 
    '/log', 'log',
    '/code', 'code',
    '/phone', 'phone',
)
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()