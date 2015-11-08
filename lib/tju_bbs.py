#!/usr/bin/env python
# -*- coding: gbk -*-

'''auto bbs'''
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re
import time

# import sae 

class Tjubbs(object):
	def __init__(self,session_id=None,cookie=False):
		self.base_url = "http://bbs.tju.edu.cn"
		self.login_url = "http://bbs.tju.edu.cn/TJUBBS/bbslogin"
		self.headers = {
			'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',  
			'Referer' : self.base_url,
			} 
		self.session_id = session_id
		self.cookie = cookie


	def login(self,account_id,account_pw):

		if self.cookie:
			cj = cookielib.LWPCookieJar()
			cookie_support = urllib2.HTTPCookieProcessor(cj)
			opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
			urllib2.install_opener(opener)
			h = urllib2.urlopen(self.base_url)
		  
		loginData = {'id' : account_id,  
		            'pw' : account_pw,  
		            'button.x' : '38',  
		            'button.y' : '7',   
		            }
		loginData = urllib.urlencode(loginData)
		request = urllib2.Request(self.login_url, loginData, self.headers)
		response = urllib2.urlopen(request)
		res_str = response.read()
		find_session = re.search('url=/.+/',res_str)
		
		if find_session:
			self.session_id = find_session.group(0)[5:-1]
			self.is_login = True
			return "LoginSuccess"
		else:
			return "LoginFailed"

	def post(self,board,article):
		if not self.session_id:
			return "LogInRequired"

		postData = {
			'title': article['title'],
			'text': article['text'],
		}
		if board=='LostFound':
			postData['tmpl'] = 2

		post_url = "{0}/{1}/{2}".format(self.base_url,self.session_id,'bbssnd?board='+board+'&th=-1')

		postData = urllib.urlencode(postData)
		request = urllib2.Request(post_url, postData, self.headers)
		response = urllib2.urlopen(request)
		res_str = response.read()

		if 'Refresh' in res_str:
			return "PostSucceess"
		elif '请先登录' in res_str:
			return "LogInRequired"
		elif '间隔过密' in res_str:
			return "TooFast"
		else:
			return "UnkownError"

def tju_format(card_id,name,contact_name="",contact_phone="",msg=""):
	card_id = card_id.encode('gbk')
	name = name.encode('gbk')
	contact_name = contact_name.encode('gbk')
	contact_phone = contact_phone.encode('gbk')
	msg = msg.encode('gbk')
	desc_name = "*{0}*同学尾号为{1}的天大校园卡".format(name,card_id[-4:])
	post_date = time.strftime("%Y.%m.%d")
	pick_loc = "无"
	event_desc = "有人捡到了你的校园卡,并且通过yunyin.org发布了招领启事"
	if contact_phone or contact_name:
		contact_info = contact_name + '[' + contact_phone + ']'
	else:
		contact_info = "他没有提供联系方式"
	note = msg
	return format_lost_found(desc_name,post_date,pick_loc,event_desc,contact_info,note)


def format_lost_found(name,date="",loc="",desc="",cont="",note=""):
	post_data = {}
	post_data['title'] = "【招领】招领" + name
	post_data['text'] = '''[1;31m【招领物品名称】:[0m {0}
[1;32m【拾到物品时间】:[0m {1}
[1;33m【拾到物品地点】:[0m {2}
[1;34m【事件简要说明】:[0m {3}
[1;35m【联系方式】:[0m {4}
[1;36m【其他说明事项】:[0m {5}
-------------------------------------
此消息由yunyin.org自动发出'''.format(name,date,loc,desc,cont,note)
	return post_data

def test():
	bbs = Tjubbs()
	bbs.login('yunyin','789456123')
	a = format_lost_found('王同学尾号为4510的天大校园卡',"2012.01.12","无","有人捡到了你的校园卡,并且通过yunyin.org发布了招领启事","15822882341 如花","再不来取我就把他放在学一食堂了")
	bbs.post('test',a['title'],a['text'])

