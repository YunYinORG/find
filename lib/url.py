#!/usr/bin/env python
# coding=utf-8
from json import loads
import uuid
import urllib2
from config import VIEW_BASE as BASE_URL, WEIBO_KEY
__doc__ = "短链接管理"


def create(find_id, lost_id):
    """创建快速找回URL"""
    head = str(lost_id) + hex(int(find_id))[1:]
    s = uuid.uuid1().__str__().replace('-', '')
    token = head + s[0:(32 - len(head))]
    return token, BASE_URL + '?t=' + token


def short(url):
    """创建短链接"""
    apiurl = 'https://api.weibo.com/2/short_url/shorten.json?source=%s&url_long=%s' % (WEIBO_KEY, url)
    req = urllib2.Request(apiurl)
    response = urllib2.urlopen(req)
    result = response.read()
    try:
        result = loads(result)  # 转成对象
        return result['urls'][0]['url_short'][7:]
    except Exception:
        return "find.yunyin.org"
