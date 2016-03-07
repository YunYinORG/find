#!/usr/bin/env python
# coding=utf-8
from index import index
from notify import notify, broadcast
from phone import phone, code
from record import record, report, detail, view
from found import found
from school import *
# url路由
urls = (
    '/', 'index',  # 首页
    '/notify/', 'notify',  # 通知
    '/notify/broadcast', 'broadcast',  # 广播
    '/phone/', 'phone',  # 绑定手机
    '/phone/code', 'code',  # 手机验证码验证
    '/record/', 'record',  # 查看记录
    '/record/report', 'report',  # 举报
    '/record/detail', 'detail',  # 感谢
    '/found/','found',    #丢失信息 
    '/record/v/', 'view',  # 免登录查看
    '/school/nku', 'nku',  # 学校
    '/weibo', 'weibo',  # 绑定weibo账号
    '/test', 'test',  # 可用性测试
)
