#!/usr/bin/env python
#coding=utf-8
import web

class index:
	def GET(self):
		html = web.template.frender('templates/index.html')
		return html()