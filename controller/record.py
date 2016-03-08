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
    return m.strip()

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
      
        data = web.input(id=None,status=0,token=None)
        if not data.status or not data.id:
            return json(0, '信息不完整')
        elif data.token:
            record= recordModel.find(data.id,'find_id,status', token=data.token)
        else:
            uid = getUserId()
            record = recordModel.find(data.id,'find_id,status', lost_id=uid)


        if not record:
            return json(0, '记录已不存在')
        elif record.status != 0:
            return json(0, '记录已经修改，如需要再次修改,请联系feedback@yunyin.org')
        elif int(data.status)==1:
            #感谢
            #发送感谢短信
            recordModel.save(data.id, status=1)
            return json(1,'已发送感谢')
        elif int(data.status)==-1:
            #举报
            userModel.save(record.find_id,status=-1)
            recordModel.save(data.id, status=-1)
            return json(1,'已举报')
        else:
            return json(0,'状态更新失败')


class view:

    """免登录查看单记录查看页"""

    def GET(self):
        """免登录记录查看，参数token"""
        token = web.input(t=None).t
        if not token:
            return "无限查看"

        record = recordModel.find('id,lost_id,find_id,time,way,token,status', token=token)
       
        if not record:
            return "此临时页面已关闭"
        else:
            record.ways=parseWay(record.way)
            finder = userModel.find(record.find_id, 'id,name,phone')
            lost = userModel.find(record.lost_id, 'id,name,number,school')
            lost.school = config.SCHOOL[lost.school or 0]
            html = web.template.frender('templates/record/detail.html')
            return html(record, finder, lost,token)

class detail:
    def GET(self):
        """记录详情查看"""
        uid = getUserId()
        rid = web.input(id=None).id
        record = recordModel.find(rid,'id,lost_id,find_id,time,status,way', lost_id=uid)
        if not record:
            raise web.seeother("/")
        
        record.ways=parseWay(record.way)
        finder = userModel.find(record.find_id, 'id,name,phone')
        lost = userModel.find(record.lost_id, 'id,name,number,school')
        lost.school = config.SCHOOL[lost.school or 0]
        html = web.template.frender('templates/record/detail.html')
        return html(record, finder, lost)