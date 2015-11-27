#!/usr/bin/env python
# coding=utf-8
import web
import urllib
import urllib2
from json import loads
from config import YUNYIN_API as BASE_URL, YUNYIN_KEY as APIKEY

# BASE_URL = config.YUNYIN_API
# APIKEY = config.YUNYIN_KEY


def _get(url):
    """get 请求数据"""
    token = web.cookies().get('token')
    if not token:
        return False
    else:
        h = {'Cookie': 'token=%s' % (token)}
        req = urllib2.Request(url, headers=h)
        response = urllib2.urlopen(req)
        result = response.read()
        try:
            return loads(result)  # 转成对象
        except Exception:
            return None


def _post(url, data=None):
    """post 请求"""
    if not data:  # 无数据
        req = urllib2.Request(url)
    else:
        post_data = urllib.urlencode(data)
        token = web.cookies().get('token')
        if token:  # 带上cookietoken
            h = {'Cookie': 'token=%s' % (token)}
            req = urllib2.Request(url, post_data, headers=h)
        else:
            req = urllib2.Request(url, data)
    try:
        response = urllib2.urlopen(req)
        result = response.read()
        result = loads(result)
        return result
    except Exception:
        return None


def getUser():
    """查询当前用户状态"""
    url = BASE_URL + 'user'
    result = _get(url)
    if not result:
        return False
    elif result['status'] == 1 and result['info']:
        return result['info']['user']
    else:
        return None


def getDetail(yyid):
    """查询当前用户学号"""
    url = BASE_URL + 'user/' + str(yyid)
    result = _get(url)
    if not result:  # 请求失败
        return False
    elif result['status'] == 1:  # 查询操作成功
        return result['info']
    else:  # 查询操作失败
        return None


def getPhone(yyid):
    """查询当前用户的手机,返回手机号"""
    url = BASE_URL + 'user/' + str(yyid) + '/phone'
    result = _get(url)
    if not result:  # 请求失败
        return False
    elif result['status'] == 1:  # 查询操作成功
        return result['info']
    else:  # 查询操作失败
        return None


def verify(number, name, school=None):  # 返回失主信息
    """验证学号姓名"""
    url = BASE_URL + 'card'
    data = {'number': number, 'name': name, 'key': APIKEY, 'school': school}
    result = _post(url, data)
    if result:
        return result
    else:
        return None


def bindPhone(phone):
    """用户绑定手机号"""
    url = BASE_URL + 'card/phone'
    data = {'phone': phone, 'key': APIKEY}
    result = _post(url, data)
    return result
