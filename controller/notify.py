#!/usr/bin/env python
#coding=utf-8
import urllib
import urllib2
from lib.yunyin import yunyin
import settings

class notify:
	def post(self):
		number, name = web.input().number, web.input().name
		yy = yunyin()
		lost_info = yy.verify(number,name)
		if lost_info == 0 or lost_info['status'] == -1:
			return 
		else:
			if lost_info['status'] == 1:
				#发短信、邮箱
			elif lost_info['status'] == 0:
				#
				return lost_info['info']
			elif lost_info['status'] == -2:
				return '学号姓名不匹配'

	