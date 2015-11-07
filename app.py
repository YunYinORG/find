#!/usr/bin/env python
#coding=utf-8
import web
import urllib2
import urllib
urls = (
    '/', 'index',
    '/notify', 'notify',
    '/weibo', 'weibo',
    '/log', 'log',
)
app = web.application(urls, globals())

class index:
	def GET(self):
		render = web.template.render('templates/')
		return '%s' % (render.index())

class notify:
	def POST(self):
		pass

class broadcast:
	def POST(self):
		pass      
				
class verify_by_account:
	def POST(self):
		pass
		
class verify_by_phone:
	def POST(self):
		pass

if __name__ == "__main__":
    app.run()