#!/usr/bin/env python
#coding=utf-8
import web
import urllib
import urllib2
import json
import settings

BASE_URL=settings.YUNYIN_API
APIKEY=settings.YUNYIN_KEY

#get 数据
def get(url):
	token = web.cookies().get('token')
	if not token:
		return 0
	else:
		h={'Cookie':'token=%s'%(token)}
		req = urllib2.Request(url,headers=h)
		response = urllib2.urlopen(req)
		result = response.read()
		try:
			return json.loads(result)
		except Exception:
			return None

#post数据
def post(url,data=None):
	if not data:
		req = urllib2.Request(url)
	else:
		post_data = urllib.urlencode(data)
		token = web.cookies().get('token')
		if token:
			h={'Cookie':'token=%s'%(token)}
			req = urllib2.Request(url,post_data,headers=h)
		else:
			req=urllib2.Request(url,data)
	try:
		response = urllib2.urlopen(req)
		result = response.read()
		result=json.loads(result)
		return result
	except Exception:
		return None


#查询当前用户状态
def getUser():
	url=BASE_URL+'user'
	result=get(url)
	if not result:
		return None
	elif result['status']==1 and result['info']:
		return result['info']['user']
	else:
		return None

#验证学号姓名
def verify(number,name,school=None):   #失主信息
	url = BASE_URL + 'card'
	data = {'number':number, 'name':name, 'key':APIKEY,'school':school}
	result = post(url,data)
	if result:
		return result
	else:
		return None

def bind_phone():
	pass

def lost_phone(uid):
	url = BASE_URL + 'user/' + str(uid) + '/phone'
	result = self.get(url)
	if result:
		return result
	else:
		return None