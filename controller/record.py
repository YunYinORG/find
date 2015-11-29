#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user
from model import *
from config import SCHOOL
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

        record = recordModel.find('id,lost_id,find_id,time', token=token)
        if not record:
            return "此临时页面已关闭"
        else:
            finder = userModel.find(record.find_id, 'id,name,phone')
           
            lost = userModel.find(record.lost_id, 'id,name,number,school')
            lost.school = SCHOOL[lost.school]
            html = web.template.frender('templates/viewTemp.html')
            return html(record, finder, lost)
