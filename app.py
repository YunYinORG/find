#!/usr/bin/env python
# coding=utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
abspath = os.path.dirname(__file__)  # 兼容wsgi
sys.path.append(abspath)
if abspath:
    os.chdir(abspath)

import web
import lib
from controller.index import index
from controller.notify import notify, broadcast


web.config.debug = True
web.DEBUG = True
# url路由
urls = (
    '/', 'index',  # 首页
    '/notify/', 'notify',  # 通知
    '/notify/broadcast', 'broadcast',  # 广播
    '/weibo', 'weibo',  # 绑定weibo账号
    '/record', 'record',  # 查看记录
    '/phone', 'phone',  # 绑定手机
    '/phone/code', 'code',  # 手机验证码验证
    '/test', 'test',  # 可用性测试
)

N = 0


class test:

    def GET(self):
        # import json
        # return json.dumps(lib.user.getUser())
        return lib.yunyin.getPhone(12)
        # try:
        #     web.config.smtp_server = 'smtp.exmail.qq.com'
        #     web.config.smtp_port = 465
        #     web.config.smtp_username = 'test@yunyin.org'
        #     web.config.smtp_password = 'YYdebug123'
        #     web.config.smtp_starttls = True
        #     subject = '测试邮件'
        #     content = 'test'
        #     headers = {'Content-Type': 'text/html;charset=utf-8'}
        #     web.sendmail('test@yunyin.org', '353732048@qq.com', subject, content)
        #     return 1
        # except Exception, e:
        #     return e

# 启动服务
app = web.application(urls, globals())
if __name__ == "__main__":
    application = app.run()
else:
    application = app.wsgifunc()
