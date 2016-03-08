#!/usr/bin/env python
# coding=utf-8

'''NKU BBS'''
import urllib
import urllib2
import json
from config import BBS_NKU
# BBS_NKU={'group':1,'uid':1}
def _publish(article, title, uid, group_id, tags=None):
    post_data = {'uid': uid,
                 'type': "post_article",
                 'gid': group_id,
                 'name': title,
                 'content': article,
                 'anonymous': 'false',
                 'tags': tags,
                 }
    url='http://bbs.nankai.edu.cn/android/group_action/'
    post_data = urllib.urlencode(post_data)
    request = urllib2.Request(url, post_data)
    response = urllib2.urlopen(request)
    return response.read()


def _format(card_id, name, contact_name="", contact_phone="", msg=""):
    # card_id = card_id.encode('utf8')
    # name = name.encode('utf8')
    # contact_name = contact_name.encode('utf8')
    # contact_phone = contact_phone.encode('utf8')
    # msg = msg.encode('utf8')

    if contact_phone or contact_name:
        contact_info = '手机号[' + str(contact_phone)[:-8] + '********]'
    else:
        contact_info = "联系方式保密"
    article = "<p><strong>{0}</strong>同学,卡号{1}的一卡通被 {2} 捡到了!!!<br/>{2} 的留言是：{3} <br/>联系方式：{4}。<br/>为了保护拾卡者隐私，部分信息已隐藏。失主凭学号进入<a href='http://find.yunyin.org/school/nku'>find.yunyin.org/school/nku</a>查看完整联系信息<br/></p><p style='text-align:right;color:rgb(178,178,178);'>--<small>来自<a href='http://find.yunyin.org' style='color:rgb(178,178,178);'>云印校园卡招领</a>自动发布</small></p>".format(name, card_id, contact_name, msg, contact_info)
    return article

def post(card_id,name,contact_name,phone="",msg=""):
	title= "【失物招领】[{0}]同学尾号为{1}的一卡通".format(name, card_id[-4:])
	article= _format(card_id, name, contact_name, phone, msg)
	response= _publish(article, title,BBS_NKU['uid'] , BBS_NKU['group'], "失物招领,云印招领服务")
	response= response and json.loads(response)
	if response and response['status']==1:
		return True
	else:
		return False