#!/usr/bin/env python
#coding=utf-8
import web
import settings
import urllib
import urllib2

class yunyin:
	def __init__(self,apikey='',url='http://api.yunyin.org/'):
		self.base_url = url
		self.apikey=apikey

	def logged(self):
		url = self.base_url + 'user'
		result = self.get(url)
		if result:
			return result
		else:
			return 0

	def verify(self,number,name):   #失主信息
		url = self.base_url + 'card'
		data = {'number':number, 'name':name, 'apikey':APIKEY}
		result = post(url,data)
		if result:
			return result
		else:
			return 0

	def lost_phone(self,uid):
		url = self.base_url + 'user/' + str(uid) + 'phone'
		result = self.get(url)
		if result:
			return result
		else:
			return 0

	def bind_phone(self):
		pass

	def getUser(self):
		url=self.base_url+'user'
		return self.get(url)

	@staticmethod
	def post(url,data):
		token = web.cookies().get('token')
		if not token:
			return 0
		else:
			header = {'TOKEN':token}
			post_data = urllib.urlencode(data)
			req = urllib2.request(url,post_data,header)
			response = urllib2.urlopen(req)
			result = response.read()
			return result

	@staticmethod
	def get(url):
		token = web.cookies().get('token')
		if not token:
			return 0
		else:
			h={'Cookie':'token=%s'%(token)}
			req = urllib2.Request(url,headers=h)
			response = urllib2.urlopen(req)
			result = response.read()
			return result