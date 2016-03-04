#!/usr/bin/env python
# -*- coding: utf-8 -*

import urllib2
import urllib
import re
from config import WEIBO_COOKIE


def fetch(url, data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Referer': '',
        'Cookie': WEIBO_COOKIE
    }
    if data:
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers=headers)
    else:
        req = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(req).read()


def post(content):
    homepage = fetch("http://weibo.cn/")
    sendlinks = re.compile(r'sendmblog([^<>\/].+?)"').findall(homepage)
    if len(sendlinks) > 0:
        link = "http://weibo.cn/mblog/sendmblog" + sendlinks[0]
        data={'rl': '1,', 'content': content}
        page = fetch(link, data)
        return page[:4600].find('发布成功!'.encode('utf8'))>0


def format(school, card_id, name, note=None, contact_name=None):
    if int(school) == 1:
        school_tag = "#南开大学失物招领#"
    elif int(school) == "2":
        school_tag = "#天津大学失物招领#"
    elif int(school) == "4":
        school_tag = "#河工大失物招领#"
    else:
        school_tag = ''

    if contact_name:
        picker = "{0}同学".format(contact_name.encode('utf8'))
    else:
        picker = '"雷锋同志"'

    message = "#校园卡招领中心#{0}*{1}*同学卡号为{2}的校园卡已经被{3}捡到,凭学号进入find.yunyin.org查看详细招领内容".format(school_tag, name.encode('utf8'), card_id, picker)
    if note:
        message = "%s 补充:%s" % (message, note)
    return message
