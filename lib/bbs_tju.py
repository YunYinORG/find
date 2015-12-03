#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import time
from config import BBS_TJU
__doc__ = "bbs.tju.edu.cn"
ACCOUNT = BBS_TJU['account']
PWD = BBS_TJU['pwd']


class Tjubbs(object):

    def __init__(self, session_id=None, cookie=False):
        self.base_url = "http://bbs.tju.edu.cn"
        self.login_url = "http://bbs.tju.edu.cn/TJUBBS/bbslogin"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',
            'Referer': self.base_url,
        }
        self.session_id = session_id
        self.cookie = cookie

    def login(self, account_id, account_pw):

        if self.cookie:
            cj = cookielib.LWPCookieJar()
            cookie_support = urllib2.HTTPCookieProcessor(cj)
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            h = urllib2.urlopen(self.base_url)

        loginData = {'id': account_id, 'pw': account_pw, 'button.x': '38', 'button.y': '7', }
        loginData = urllib.urlencode(loginData)
        request = urllib2.Request(self.login_url, loginData, self.headers)
        response = urllib2.urlopen(request)
        res_str = response.read()
        find_session = re.search('url=/.+/', res_str)

        if find_session:
            self.session_id = find_session.group(0)[5:-1]
            self.is_login = True
            return "LoginSuccess"
        else:
            return "LoginFailed"

    def post(self, board, article):
        if not self.session_id:
            return "LogInRequired"
        postData = {
            'title': article['title'],
            'text': article['text']
        }
        if board == 'LostFound':
            postData['tmpl'] = 2

        post_url = "{0}/{1}/{2}".format(self.base_url, self.session_id, 'bbssnd?board=' + board + '&th=-1')

        postData = urllib.urlencode(postData)
        request = urllib2.Request(post_url, postData, self.headers)
        response = urllib2.urlopen(request)
        res_str = response.read()

        if 'Refresh' in res_str:
            return True  # "PostSucceess"
        elif '请先登录' in res_str:
            return False  # "LogInRequired"
        elif '间隔过密' in res_str:
            return False  # "TooFast"
        else:
            return False  # "UnkownError"


def format_lost_found(name, loc="", desc="", cont="", note=""):
    post_data = {}
    post_data['title'] = ("【招领】招领" + name).encode('gbk')
    text = ''' 
 【招领物品名称】: {0}
 【拾到物品时间】: {1}
 【拾到物品地点】: {2}
 【事件简要说明】: {3}
 【联系方式】: {4}
 【其他说明事项】: {5}
-------------------------------------
此消息由find.yunyin.org联系失主失败后自动发出'''.format(name, time.strftime("%Y.%m.%d"), (loc or note), desc, cont, note)
    post_data['text'] = text.encode('gbk')
    return post_data

bbs = Tjubbs()
bbs.login(ACCOUNT, PWD)


def broadcast(card, name, viewurl, note=None, finderName="隐私保护"):
    """发送招领公告"""
    desc_name = "*{0}*[{1}]的校园卡".format(name, card)
    event_desc = "有人捡到了您的校园卡,无法通过手机联系到您,发送此招领广播" + viewurl
    article = format_lost_found(desc_name, desc=event_desc, cont=finderName, note=note)
    if not bbs.post('LostFound', article):
        bbs.login(ACCOUNT, PWD)
        return bbs.post('LostFound', article)
    else:
        return True
