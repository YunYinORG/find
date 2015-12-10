#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user
from lib.response import json as json
from model import userModel, recordModel
import config
"""记录查看管理页"""


def getUserId():
    u = user.getUser()
    if not u:
        raise web.seeother("/")
    else:
        return u['id']

def parseWay(way):
    m=''
    if way&config.NOTIFY_SMS:
        m+=' 发送短信 '
    if way&config.NOTIFY_MAIL:
        m+=' 发送邮件 '
    if way&config.NOTIFY_WEIBO:
        m+=' 微博广播 '
    if way&config.NOTIFY_BBS:
        m+=' 校内BBS '
    return m

class record:

    def GET(self):
        """记录页"""
        uid = getUserId()
        #丢失记录
        lost = recordModel.select(lost_id=uid)
        if lost:
            for l in lost:
                u = userModel.find(l.find_id, 'name,phone')
                if u:
                    l.finder = u.name
                    l.phone = u.phone
                    l.way =parseWay(l.way)
                else:
                    del l
        find = recordModel.select(find_id=uid)
        #捡卡记录
        if find:
            for f in find:
                u = userModel.find(f.lost_id, 'name,number')
                if u:
                    f.loster = u.name
                    f.card = u.number
                    f.way =parseWay(f.way)
                else:
                    del f
        html = web.template.frender('templates/record/index.html')
        return html(lost, find)


class report:

    def POST(self):
        """举报,参数ID"""
        uid = getUserId()
        data = web.input(id=None, status=0)
        if not data.id or not data.status:
            return json(0, '信息不完整')

        record = recordModel.find('status', id=data.id, lost_id=uid)
        if not record:
            return 0
        elif record.status != 0:
            return -1
        elif recordModel.save(record_id, status=data.status):
            return 1
        else:
            return -2


class thank:

    def POST(self):
        """感谢,参数ID"""
        return web.input(id=None).id


class view:

    """免登录查看单记录查看页"""

    def GET(self):
        """免登录记录查看，参数token"""
        token = web.input(t=None).t
        if not token:
            return "无限查看"

        record = recordModel.find('id,lost_id,find_id,time,way', token=token)
        if not record:
            return "此临时页面已关闭"
        else:
            finder = userModel.find(record.find_id, 'id,name,phone')
            lost = userModel.find(record.lost_id, 'id,name,number,school')
            lost.school = config.SCHOOL[lost.school or 0]
            html = web.template.frender('templates/record/view.html')
            return html(record, finder, lost)

class detail:
    def GET(self):
        """记录详情查看"""
        uid = getUserId()
        rid = web.input(id=None).id
        record = recordModel.find(rid,'id,lost_id,find_id,time,status,way', lost_id=uid)
        if not record:
            raise web.seeother("/")
        
        finder = userModel.find(record.find_id, 'id,name,phone')
        lost = userModel.find(record.lost_id, 'id,name,number,school')
        lost.school = config.SCHOOL[lost.school or 0]
        html = web.template.frender('templates/record/detail.html')
        return html(record, finder, lost)