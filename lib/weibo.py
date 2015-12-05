#!/usr/bin/env python
# -*- coding: utf-8 -*

import urllib2
import urllib
import cookielib
import re
from config import WEIBO_ACCOUNT, WEIBO_PWD


class Fetcher(object):

    def __init__(self, username=None, pwd=None, cookie_filename=None):
        self.cj = cookielib.LWPCookieJar()
        if cookie_filename is not None:
            self.cj.load(cookie_filename)
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.cookie_processor, urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)

        self.username = username
        self.pwd = pwd
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        'Referer': '', 'Content-Type': 'application/x-www-form-urlencoded'}

    def get_rand(self, url):
        urlre = re.compile(r'form action="([^<>\/].+?)"')
        vkre = re.compile(r'name="vk" value="([^<>\/].+?)"')
        passwdre = re.compile(r'type="password" name="([^<>\/].+?)"')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows;U;Windows NT 5.1;zh-CN;rv:1.9.2.9)Gecko/20100824 Firefox/3.6.9', 'Referer': ''}
        req = urllib2.Request(url, "", headers)
        login_page = urllib2.urlopen(req).read()
        url = urlre.findall(login_page)[0]
        passwd = passwdre.findall(login_page)[0]
        vk = vkre.findall(login_page)[0]
        return url, passwd, vk

    def login(self, username=None, pwd=None, cookie_filename=None, content=None):
        if self.username is None or self.pwd is None:
            self.username = username
            self.pwd = pwd
        url = 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F%3Ffrom%3Dindex%26rl%3D1%26luicode%3D20000173&backTitle=%CE%A2%B2%A9&vt=4'
        # 获取随机数rand、password的name和vk
        url, passwd, vk = self.get_rand(url)
        url = 'http://login.weibo.cn/login/' + url
        data = urllib.urlencode({'mobile': self.username,
                                 passwd: self.pwd,
                                 'backURL': 'http%3A%2F%2Fweibo.cn%2F%3Ffrom%3Dindex%26amp%3Brl%3D1%26amp%3Bluicode%3D20000173',
                                 'backTitle': '微博',
                                 'tryCount': '',
                                 'vk': vk,
                                 'submit': '登录', })

        # 模拟提交登陆
        self.fetch(url, data)
        page = self.fetch("http://weibo.cn/", data)
        linkre = re.compile(r'sendmblog([^<>\/].+?)"')
        link = "http://weibo.cn/mblog/sendmblog" + linkre.findall(page)[0]
        data = urllib.urlencode({'rl': '1,', 'content': content})
        page = self.fetch(link, data)
        return page.find('发布成功') > 0

    def fetch(self, url, data):
        req = urllib2.Request(url, data, headers=self.headers)
        return urllib2.urlopen(req).read()

weibo = Fetcher()


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

    message = "#云印南天校园卡招领中心#{0}*{1}*同学卡号为{2}的校园卡已经被{3}捡到,凭学号进入find.yunyin.org查看详细招领内容".format(school_tag, name.encode('utf8'), card_id, picker)
    if note:
        message = "%s 补充:%s" % (message, note)
    return message


def post(text):
    return weibo.login(WEIBO_ACCOUNT, WEIBO_PWD, "", text)
