#!/usr/bin/env python
# coding=utf-8
from index import index
from notify import notify, broadcast
from phone import phone, code

# url路由
urls = (
    '/', 'index',  # 首页
    '/notify/', 'notify',  # 通知
    '/notify/broadcast', 'broadcast',  # 广播
    '/weibo', 'weibo',  # 绑定weibo账号
    '/record', 'record',  # 查看记录
    '/phone/', 'phone',  # 绑定手机
    '/phone/code', 'code',  # 手机验证码验证
    '/test', 'test',  # 可用性测试
)
