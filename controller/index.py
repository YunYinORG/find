#!/usr/bin/env python
#coding=utf-8
import web
# session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
class index:
	def GET(self):
		html = web.template.frender('templates/index.html')
		return html()