#!/usr/bin/env python
# coding=utf-8

import web
from random import randint
from lib.response import json
from lib import cookie, yunyin, sms, user, validate


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
                data['type'] = 0
        elif not validate.name(data['name']):  # 验证姓名格式
            return json(0, "姓名无效")
        else:  # 验证数据类型
            data['type'] = 1

        # 检查手机是否存在

        # 生成验证码发送
        code = str(randint(1000, 999999))
        if sms.sendBind(data['phone'], code):
            data['code'] = code
            cookie.set('phone', data)
            return json(1, '验证码已经发送成功')
        else:
            return json(0, '验证码发送失败')


class code:
    # todo：check the phone exist or not

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
                user.saveUser(data['name'], 0, data['phone'])
                return json(1, data['name'])
            elif yunyin.bindPhone(data['phone']):  # 绑定手机
                return json(1, '手机绑定完成')
            else:
                return json(-1, '手机信息和云印API同步出错,如果绑定过云印南天账号，请直接使用该账号登录')
