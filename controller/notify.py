#!/usr/bin/env python
# coding=utf-8
import web
from lib import yunyin, user, validate, cookie
from lib.response import json
"""通知"""

NO_USER = 2
SUCCESSS = 1
UNLOGIN = 0
RETRY = -1
NO_PHONE = -2


class notify:

    def POST(self):
        """验证通知"""
        info = web.input(number=None, name=None)
        school = validate.school(info['number'])
        if info.name == None or info.number == None:  # 输入无效
            return json(-5, "数据无效")
        elif not user.getUser():      # 未登录
            return json(UNLOGIN, "未登录")
        elif not school > 0:  # 学号格式错误
            return json(RETRY, "学号格式不对")
        elif not validate.name(info['name']):  # 姓名错误
            return json(RETRY, "请输入正确姓名")
        else:  # 输入正常
            phone = user.getPhone()
            if not phone:
                return json(NO_PHONE, "需要验证手机后使用")

            data = yunyin.verify(info['number'], info['name'], school)
            if not data:  # 查询失败
                return self.next(info, school, 0)
            elif data['status'] == -2:  # 验证不匹配
                return json(RETRY, "验证不匹配")
            elif data['status'] != 1:  # 无该用户
                return self.next(info, school, 0)
            else:  # 验证成功
                lost = data['info']

                if lost['phone'] and self.phoneNotify(lost['phone']):
                    return json(SUCCESSS, "通知成功")
                elif lost['email']:  # 发送邮件

                    return self.next(info, school, 1)
                else:  # 联系方式
                    return 1

    def GET(self):
        return json(0, 'only post allowed')

    def next(self, info, school, is_yunyin_user=0):  # 无手机号转入下一步
        data = {'name': info['name'], 'card': info['number'], 'sch': school, 'in': is_yunyin_user}
        cookie.set('b', data)
        return json(NO_USER, school)


class broadcast:

    def POST(self):
        """发送广播"""
        data = cookie.get('b')
        if not data:
            return json(0, '验证信息无效')
        else:
            cookie.delete('b')
            return json(1, '发送成功')
