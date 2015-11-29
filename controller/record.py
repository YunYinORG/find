#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user
from model import *
"""记录查看管理页"""


class record:

    def GET(self):
        """记录页"""
        return "记录页"


class report:

    def POST():
        """举报,参数ID"""
        return web.input(id=None).id


class thank:

    def POST():
        """感谢,参数ID"""
        return web.input(id=None).id


class view:

    """免登录查看单记录查看页"""

    def GET(self):
        """免登录记录查看，参数token"""
        token = web.input(t=None).t
        if not token:
            return "无限查看"

        record = recordModel.find(token=token)
        if not record:
            return "访问信息无效"
        else:
            finder = userModel.find(record.find_id, 'id,name,phone')
            html = web.template.frender('templates/viewTemp.html')
            return html(record, finder)
