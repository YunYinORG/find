#!/usr/bin/env python
# coding=utf-8

import web
from lib import cookie, yunyin, sms, user, validate
from lib.response import json
from model.user import userModel
"""手机号验证和登录[done]"""


class phone:

    def POST(self):
        """验证手机号"""
        data = web.input(phone=None, name=None)

        if not validate.phone(data['phone']):  # 手机号无效
            return json(0, "号码无效")
        elif user.getUser():  # 判断是否登录
            if user.getPhone():  # 已登录不可修改手机
                return json(-1, "已经绑定过手机")
            else:  # 绑定手机
                dbuser = userModel.find('yyid', phone=data['phone'])
                if dbuser and dbuser.yyid:
                    return json(-1, "一个手机只能绑定一个用户")
                else:
                    data['type'] = 0
                    code = sms.sendBind(data['phone'])
        elif not validate.name(data['name']):  # 验证姓名格式
            return json(0, "姓名无效")
        else:  # 临时登录
            data['type'] = 1
            code = sms.sendLogin(data['phone'])

        if code:
            data['code'] = code
            cookie.set('phone', data)
            return json(1, '验证码已经发送成功')
        else:
            return json(0, '验证码发送失败')


class code:

    def POST(self):
        """ 验证验证码   """
        code = web.input(code=None)['code']
        if not code:
            return json(0, '验证码错误')
        else:
            data = cookie.get('phone')
            cookie.delete('phone')
            if not data:
                return json(-1, '验证信息不存在')
            elif data['code'] != code:
                return json(-1, '验证码错误请重新发送')
            elif data['type'] == 1:  # 临时登录
                name = data['name']
                dbuser = userModel.find('id,yyid,name', phone=data['phone'])
                if not dbuser:  # 数据库中不存在
                    uid = userModel.add(name=name, phone=data['phone'])
                    user.saveUser(uid, name, data['phone'])
                elif not dbuser.yyid:  # 数据库中的临时用户
                    userModel.save(dbuser.id, name=name)
                    user.saveUser(uid, name, data['phone'])
                else:  # 数据库中存在的云印用户
                    name = dbuser.name
                    user.saveUser(uid, name, data['phone'], yyid)
                return json(1, name)
            elif yunyin.bindPhone(data['phone']):  # 绑定手机
                user.savePhone(data['phone'])
                return json(1, '手机绑定完成')
            else:  # 数据绑定失败
                return json(-1, '手机信息和云印API同步出错,如果绑定过云印南天账号，请直接使用该账号登录')
