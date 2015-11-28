#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user
from model.record import recordModel
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
        """记录查看，参数token"""
        return web.input(token=None).token
