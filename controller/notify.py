#!/usr/bin/env python
#coding=utf-8
import web
import json
# from lib.yunyin import yunyin

# import settings

class notify:
	def POST(self):
		info= web.input(number=None,name=None)
		# yy = yunyin()
		# lost_info = yy.verify(number,name)
		# if lost_info == 0 or lost_info['status'] == -1:
		# 	return 
		# else:
		# 	if lost_info['status'] == 1:
		# 		#发短信、邮箱
		# 	elif lost_info['status'] == 0:
		# 		#
		# 		return lost_info['info']
		# 	elif lost_info['status'] == -2:
		# 		return '学号姓名不匹配'
		response={};
		response['status']=0;
		web.header('Content-Type', 'application/json')
		return json.dumps(response)

	def GET(self):
		return 'only post allowed'

class broadcast:
	def POST(self):
		return "post"

	def GET(self):
		return "GET"

	