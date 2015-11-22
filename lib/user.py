#!/usr/bin/env python
#coding=utf-8
import web
import yunyin as yy

#获取当前的用户名
def getName():
	# name=web.session(name=False)
	current_user=yy.getUser()
	if not current_user:
		return False
	else:
		return current_user['name']
#获取当前用户的id
def getId():
	current_user=yy.getUser()
	if current_user:
		return current_user['id']
	else:
		return None

#获取电话
def getPhone():
	return False

