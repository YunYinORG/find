#!/usr/bin/env python
#coding=utf-8
import web
import json
from lib.yunyin import yunyin
from lib.user import user
# import settings

class notify:
	def POST(self):
		info= web.input(number=None,name=None)
		response={};
		
		if info.name==None or info.number==None:
			#输入无效
			response['status']=-5
			response['message']="数据无效"
		elif not user.getId():
			#未登录
			response['status']=0
			response['message']="未登录"
		else:
			response['status']=1
			response['message']="发送"
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

		web.header('Content-Type', 'application/json')
		return json.dumps(response)

	def GET(self):
		return 'only post allowed'

class broadcast:
	def POST(self):
		return "post"

	def GET(self):
		return "GET"

	