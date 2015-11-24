#!/usr/bin/env python
# coding=utf-8
import web
import json
from lib import yunyin, user
# import settings
SUCCESSS = 1
NODATA = 2
UNLOGIN = 0
NOPHONE = -1
RETRY = 1


class notify:

    def POST(self):
        info = web.input(number=None, name=None)
        response = {}
        if info.name == None or info.number == None:
            # 输入无效
            response['status'] = -5
            response['message'] = "数据无效"
        elif not user.getUser():
            # 未登录
            response['status'] = 0
            response['message'] = "未登录"
        else:
            phone = user.getPhone()
            if not phone:
                response['status'] = -1

            data = yunyin.verify(info['number'], info['name'])
            if not data:
                response['status'] = 2
                response['school'] = 1
                response['message'] = "无相关信息"
            elif data['status'] == 1:  # 验证成功
                response['status'] = 1
                response['message'] = "发送成功!"
            elif data['status'] == -2:  # 验证不匹配
                response['status'] = -1
            else:
                response['status'] = 2

        # yy = yunyin()
        # lost_info = yy.verify(number,name)
        # if lost_info == 0 or lost_info['status'] == -1:
        # 	return
        # else:
        # 	if lost_info['status'] == 1:
        # 		#发短信、邮箱
        # 	elif lost_info['status'] == 0:
        # 		#
        # 		return lost_info['info']
        # 	elif lost_info['status'] == -2:
        # 		return '学号姓名不匹配'
        web.header('Content-Type', 'application/json')
        return json.dumps(response)

    def GET(self):
        return 'only post allowed'


class broadcast:

    def POST(self):
        return "post"

    def GET(self):
        return "GET"
