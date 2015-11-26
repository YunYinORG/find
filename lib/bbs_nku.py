#!/usr/bin/env python
#coding=utf-8

'''auto bbs'''
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import time


class Nkubbs(object):
	def __init__(self,uid):
		self.article_url = 'http://bbs.nankai.edu.cn/android/group_action/'
		self.uid = uid

	def post(self,board_id,article,tags):
		headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',  
           'Referer' : self.article_url}

		post_data = {'uid' : self.uid,  
            'type' : "post_article",  
            'gid' : board_id,  
            'name' : article['title'],
            'content':article['text'],
			'anonymous':'false',
			'tags': tags,
            }        

		post_data = urllib.urlencode(post_data)
		request = urllib2.Request(self.article_url, post_data, headers)
		response = urllib2.urlopen(request)
		res_str = response.read()

		if '1' in res_str:
			return "PostSucceess"
		else:
			return "UnkownError"

def nku_format(card_id,name,contact_name="",contact_phone="",msg=""):
	card_id = card_id.encode('utf8')
	name = name.encode('utf8')
	contact_name = contact_name.encode('utf8')
	contact_phone = contact_phone.encode('utf8')
	msg = msg.encode('utf8')
	post_data = {}
	post_data['title'] = "【失物招领】[{0}]同学尾号为{1}的一卡通".format(name,card_id[-4:])
	if contact_phone or contact_name:
		contact_info = '手机号[' + contact_phone + ']'
	else:
		contact_info = "联系方式保密"
	post_data['text'] = "<p><strong>{0}</strong>同学,尾号为{1}的南开校园一卡通被 {2} 捡到了!!!<br/>{2} 的留言是：{3} <br/>联系方式：{4}。<br/></p><p style='text-align: right;'>--来自<a href='http://yunyin.org/Card/'>云印校园卡招领</a>自动发布</small></p>\
						".format(name,card_id[-4:],contact_name,msg,contact_info)
	return post_data
