#!/usr/bin/env python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")  # 设置编码

import os
abspath = os.path.dirname(os.path.abspath(__file__))  # 获取绝对路径
sys.path.append(abspath)  # 兼容wsgi
os.chdir(abspath)  # 更新目录

import web
from controller import *

web.config.debug = True
# 启动服务
app = web.application(urls, globals())
if __name__ == "__main__":  # python直接启动服务
    application = app.run()
else:  # wsgi模式启动
    application = app.wsgifunc()


class test(object):

    def GET(self):
        return "it works"
