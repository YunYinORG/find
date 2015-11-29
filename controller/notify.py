#!/usr/bin/env python
# coding=utf-8
import web
from lib import sms, yunyin, user, validate, cookie
from lib.response import json
import lib.url as url
from model.user import userModel, merge
from model.record import recordModel
"""通知"""

NO_USER = 2
SUCCESSS = 1
UNLOGIN = 0
RETRY = -1
NO_PHONE = -2
LIMITED = -3
RECORD_SMS = 1


class notify:
    # TODO 屏蔽和账号封禁检查

    def POST(self):
        """验证通知"""
        # 检查登录
        finder = user.getUser()
        if not finder:  # 未登录
            return json(UNLOGIN, "未登录")

        # 检查输入
        info = web.input(number=None, name=None)
        status, school = notify.checkInput(info)
        if not (status is True):  # 输入有误
            return json(status, school)

        # 检查手机号和查找人的账号
        phone = user.getPhone()
        if not phone:
            return json(NO_PHONE, "需要验证手机后使用")
        elif not notify.checkFind(finder['id'], finder['yyid']):
            return json(LIMITED, "当前账号被举报封禁或者超过大尝试次数[存在未确认的记录]")

        # 验证失主信息
        data = yunyin.verify(info['number'], info['name'], school)
        if not data:  # 查询失败
            return self.next(info, school, 0)
        elif data['status'] == -2:  # 验证不匹配
            return json(RETRY, "验证不匹配")
        elif data['status'] != 1:  # 无该用户
            return self.next(info, school, 0)
        else:  # 验证成功
            lost = data['info']

        if not lost['phone']:  # 验证成功，但无手机号
            if not db_yy_user:  # 无本地账户，创建用户
                userModel.add(yyid=lost['id'], name=lost['name'], school=lost['sch_id'], type=1)
            return self.next(info, school, 1)
        elif phone == lost['phone']:  # 寻找者与失主同号，自己测试
            return json(-5, "请不要用自己的账号测试！")
        else:  # 有手机号
            # 更新本地数据库
            lost_id = notify.sync(lost)
            if not lost_id:
                return json(-5, "失主学号在系统中数据异常")

            # 失主状态检查
            if not notify.checkLost(lost_id):
                return json(LIMITED, '失主未确认记录过多，或者设置了防骚扰，禁止发送通知')

            # 发送短信
            token, long_url = url.create(finder['id'], lost_id)
            if sms.sendNotify(lost['phone'], finder['name'], phone, url.short(long_url)):  # 短信发送通知
                recordModel.add(lost_id=lost_id, find_id=finder['id'], way=RECORD_SMS, token=token)
                return json(SUCCESSS, "通知成功")
            else:  # 发送失败
                return self.next(info, school, 1)

    def GET(self):
        return json(0, 'only post allowed')

    def next(self, info, school, is_yunyin_user=0):
        """无手机号转入下一步"""
        data = {'name': info['name'], 'card': info['number'], 'sch': school, 'in': is_yunyin_user}
        cookie.set('b', data)
        return json(NO_USER, is_yunyin_user and school)

    @staticmethod
    def checkFind(uid, userType):
        """检查查找者的状态"""
        finder = userModel.find(uid, 'status')
        if not finder:
            return False
        elif finder.status < 1:  # 此账号已封禁
            return False
        # 检查未找回记录
        times = recordModel.count(find_id=int(uid), status=0)
        if userType:
            return times < 3
        else:
            return times < 1

    @staticmethod
    def checkInput(data):
        """检查输入"""
        if data.name == None or data.number == None:  # 输入无效
            return RETRY, "数据无效"
        elif not validate.name(data['name']):  # 姓名错误
            return RETRY, "请输入正确中文姓名"
        else:
            school = validate.school(data['number'])
            if school > 0:
                return True, 1
            else:  # 学号格式错误
                return RETRY, "学号格式不对"

    @staticmethod
    def sync(lost_user_in_yy):
        """同步云印账户和本地账户"""
        db_yy_user = userModel.find('id,phone', yyid=lost_user_in_yy['id'])
        if db_yy_user and db_yy_user.phone == lost_user_in_yy['phone']:  # 手机号一致
            lost_id = db_yy_user.id
        else:  # 手机号不一致
            db_phone_user = userModel.find('id,yyid', phone=lost_user_in_yy['phone'])
            if db_yy_user and not db_phone_user:  # 此云印账号已经存在数据库,但是手机号未同步
                lost_id = db_yy_user.id
                userModel.save(lost_id, phone=lost_user_in_yy['phone'])  # 更新手机
            elif db_phone_user and not db_yy_user:  # 手机存在,但此云印账号在此处不存在
                if not db_phone_user.yyid:  # 手机号为临时账号
                    lost_id = db_phone_user.id
                    userModel.save(lost_id, yyid=lost_user_in_yy['id'], number=lost_user_in_yy['number'],
                                   name=lost_user_in_yy['name'], school=lost_user_in_yy['sch_id'], type=1)
                elif db_phone_user.yyid != lost_user_in_yy['id']:  # 账号不一直在
                    # 进入此处为逻辑错误
                    # todo 删除原手机，新建账号
                    return False
            elif db_phone_user and db_yy_user:  # 两个账号同时存在
                # 合并账号
                lost_id = merge(db_phone_user.id, db_yy_user.id)
            else:  # 此账号在此处不存在,手机也不存在
                lost_id = userModel.add(yyid=lost_user_in_yy['id'], number=lost_user_in_yy['number'],
                                        name=lost_user_in_yy['name'], school=lost_user_in_yy['sch_id'], type=1)
        return lost_id

    @staticmethod
    def checkLost(lost_id):
        """检查失主账号"""
        lost_user = userModel.find(lost_id, 'blocked')
        if lost_user and lost_user.blocked:  # 关闭该功能
            return False
        elif recordModel.count(lost_id=lost_id, status=0) >= 3:  # 超过最大次数
            return False
        else:
            return True


class broadcast:

    """临时账号创建type=-1的账号"""

    def POST(self):
        """发送广播"""
        data = cookie.get('b')
        if not data:
            return json(0, '验证信息无效')
        else:
            cookie.delete('b')
            return json(1, '发送成功')
