#!/usr/bin/env python
# coding=utf-8
import web
import config
import re
from lib import sms, yunyin, user, validate, cookie
from lib.response import json
import lib.weibo_cookie as weibo
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


class notify:

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

        # 判断是否是自己的账号
        if phone == lost['phone']:
            return json(-5, "请不要用自己的账号测试！")

        # 更新本地数据库
        lost_id = notify.sync(lost)
        if not lost_id:
            return json(-5, "失主学号在系统中数据异常")
        elif not lost['phone']:  # 无手机号
            return self.next(info, school, lost_id)

        # 失主状态检查
        if not notify.checkLost(lost_id):
            return json(LIMITED, '失主未确认记录过多，或者设置了防骚扰，禁止发送通知')

        # 发送短信
        token, long_url = url.create(finder['id'], lost_id)
        if sms.sendNotify(lost['phone'], finder['name'], phone, url.short(long_url)):  # 短信发送通知
            recordModel.add(lost_id=lost_id, find_id=finder['id'], way=config.NOTIFY_SMS, token=token)
            return json(SUCCESSS, "通知成功")
        else:  # 发送失败,转到下一步
            return self.next(info, school, lost_id)

    def GET(self):
        return json(0, 'only post allowed')

    def next(self, info, school, lost_id=0):
        """无手机号转入下一步"""
        data = {'name': info['name'], 'card': info['number'], 'sch': school, 'id': lost_id}
        cookie.set('b', data)
        return json(NO_USER, lost_id and school)

    @staticmethod
    def checkFind(uid, userType):
        """检查查找者的状态"""
        finder = userModel.find(uid, 'status')
        if not finder:
            return False
        elif finder.status < 1:  # 此账号已封禁
            return False
        # 检查未找回记录
        times = recordModel.count(find_id=uid, status=0)
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
                return True, school
            else:  # 学号格式错误
                return RETRY, "学号格式不对"

    @staticmethod
    def sync(lost_user_in_yy):
        """同步云印账户和本地账户"""
        db_yy_user = userModel.find('id,yyid,phone,type', number=lost_user_in_yy['number'], school=lost_user_in_yy['sch_id'])
        if db_yy_user and not db_yy_user.yyid:  # 临时找回账号-1状态
            lost_id = db_yy_user.uid
            userModel.save(lost_id, phone=phone, type=1)
        elif db_yy_user and db_yy_user.phone == lost_user_in_yy['phone']:  # 手机号一致
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
                elif db_phone_user.yyid != lost_user_in_yy['id']:  # 账号不一致
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
        userInfo = cookie.get('b')
        if not userInfo:
            return json(RETRY, '验证信息无效')

        finder = user.getUser()
        if not user:
            return json(UNLOGIN, '未登录')
        else:
            find_id = finder['id']

        school = userInfo['sch']
        inputData = web.input(msg=None, sch=0)
        if userInfo['id'] > 0:
            uid = userInfo['id']
        elif not (inputData['sch'] and int(inputData['sch']) == school):
            return json(RETRY, '学校不匹配!')
        else:  # 创建失主临时账号
            uid = userModel.add(name=userInfo['name'], number=userInfo['card'],sch_id=school, type=-1)

        # 输入过滤
        msg = inputData['msg'] and re.sub(r'</?\w+[^>]*>', '', inputData['msg'])
        msg = msg and msg[0:16]
        way = 0x0
        token, viewurl = url.create(find_id, uid)
        # 判断学校
        if school == 1:  # 南开
            # nkbbs
            pass
        elif school == 2:  # 天大
            # tjubbs
            from lib.bbs_tju import broadcast as tjubbs_broadcast
            if tjubbs_broadcast(userInfo['card'], userInfo['name'], viewurl, msg):
                way = way | config.NOTIFY_BBS
        elif school == 4:  # 河北工业大学
            return json(LIMITED, "正在接入中")
        elif school == 3:  # 商职
            return json(LIMITED, "正在接入中")
        else:
            return json(LIMITED, "学校暂不支持")

        # 发送微博
        weibo_msg = weibo.format(school, userInfo['card'], userInfo['name'], msg)
        if weibo.post(weibo_msg):
            way = way | config.NOTIFY_WEIBO

        if way:
            # 更新数据库
            recordModel.add(lost_id=uid, find_id=find_id, way=way, token=token)
            cookie.delete('b')
            return json(SUCCESSS, way)
        else:
            return json(RETRY, '发送出错!')
