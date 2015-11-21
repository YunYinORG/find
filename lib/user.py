#!/usr/bin/env python
#coding=utf-8
import web
from yunyin import yunyin

class user(object):
	#获取当前的用户名
	@staticmethod
	def getName():
		# name=web.session(name=False)
		if not name:
			return False
	#获取当前用户的id
	@staticmethod
	def getId():
		y=yunyin()
		return y.getUser()
	
	#获取电话
	@staticmethod
	def getPhone():
		return False

