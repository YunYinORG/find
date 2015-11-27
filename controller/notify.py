#!/usr/bin/env python
# coding=utf-8
import web
from lib import sms, yunyin, user, validate, cookie
from lib.response import json
import lib.url as url
from model.user import userModel
from model.record import recordModel
"""通知"""

NO_USER = 2
SUCCESSS = 1
UNLOGIN = 0
RETRY = -1
NO_PHONE = -2
RECORD_SMS = 1


class notify:

    def POST(self):
        """验证通知"""
        info = web.input(number=None, name=None)
        school = validate.school(info['number'])
        finder = user.getUser()
        if info.name == None or info.number == None:  # 输入无效
            return json(-5, "数据无效")
        elif not finder:      # 未登录
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
                db_yy_user = userModel.find('id,phone', yyid=lost['id'])

                if lost['phone']:
                    # 更新本地数据库
                    if db_yy_user and db_yy_user.phone == lost['phone']:  # 手机号一致
                        lost_id = db_yy_user.id
                    else:  # 手机号不一致
                        db_phone_user = userModel.find('id,yyid', phone=lost['phone'])

                        if db_yy_user and not db_phone_user:  # 此云印账号已经存在数据库,但是手机号未同步
                            lost_id = db_yy_user.id
                            userModel.save(lost_id, phone=lost['phone'])  # 更新手机
                        elif db_phone_user and not db_yy_user:  # 手机也不存在,但此云印在此处不存在
                            if not db_phone_user.yyid:  # 手机号为临时账号
                                lost_id = db_phone_user.id
                                userModel.save(lost_id, yyid=lost['id'], number=lost['number'], name=lost['name'], school=lost['sch_id'], type=1)
                            elif db_phone_user.yyid != lost['id']:  # 账号不一直在
                                # 进入此处为逻辑错误
                                # todo 删除原手机，新建账号
                                return json(-5, "此学号在系统中数据异常")
                        elif db_phone_user and db_yy_user:  # 两个账号同时存在
                            # todo 合并账号
                            pass
                        else:  # 此账号在此处不存在,手机也不存在
                            lost_id = userModel.add(yyid=lost['id'], number=lost['number'], name=lost['name'], school=lost['sch_id'], type=1)

                    # 次数检查
                    # todo
                    # 准备发送短信
                    token, long_url = url.create(finder['id'], lost_id)
                    if sms.sendNotify(lost['phone'], finder['name'], phone, url.short(long_url)):  # 短信发送通知
                        recordModel.add(lost_id=lost_id, find_id=finder['id'], way=RECORD_SMS, token=token)
                        return json(SUCCESSS, "通知成功")
                    else:  # 发送失败
                        return self.next(info, school, 1)
                else:  # 验证成功但无联系方式
                        # 检查用户，创建
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
