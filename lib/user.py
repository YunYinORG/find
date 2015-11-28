#!/usr/bin/env python
# coding=utf-8
import cookie
import yunyin as yy
from model.user import merge, userModel


def _checkPhone(uid, phone):
    """检查手机号是否重复"""
    phone_user = userModel.find('id,yyid', phone=phone)
    if not phone_user:  # 手机号未登录过
        return userModel.save(uid, phone=phone)
    elif phone_user.id == uid:  # 同一个账号
        return True
    elif not phone_user.yyid:  # 临时登录过
        return merge(phone_user.id, uid)
    elif phone_user.yyid != user['yyid']:  # 异常情况,此手机已经绑定了其他账号
        return False


def saveUser(uid, name, phone=None, yyid=None):
    """保存用户信息"""
    user = {'id': uid, 'name': name, 'yyid': yyid, 'call': phone}
    return cookie.set('u', user)


def getUser():
    """获取当前的用户"""
    user = cookie.get('u')
    if user:
        return user
    else:
        yyuser = yy.getUser()  # 云印用户
        if not yyuser:
            return None
        else:
            yyid = yyuser['id']
            user = userModel.find(_field='id,phone,yyid,type', number=yyuser['number'], school=yyuser['sch_id'])
            if not user:  # 本地数据库未同步该用户
                phone = yy.getPhone(yyid)
                phone_user = phone and userModel.find('id,yyid', phone=phone)  # 云印账号带有手机
                if phone_user:  # 检查手机是否使用过
                    if not phone_user.yyid:  # 临时账号
                        uid = phone_user.id  # 更新临时账号
                        userModel.save(uid, name=yyuser['name'], number=yyuser['number'], school=yyuser['sch_id'], type=1)
                    else:  # 绑定过其他账号，账号不一致...
                        # 异常情况
                        return False
                else:
                    uid = userModel.add(yyid=yyuser['id'], name=yyuser['name'], phone=phone, number=yyuser['number'], school=yyuser['sch_id'], type=1)
            elif user.type != 1:  # 曾作为被找回临时账号,此处升级为正式账号
                uid, phone = user.id, yy.getPhone(yyid)
                userModel.save(uid, yyid=yyid, phone=phone, name=yyuser['name'], type=1)
            else:
                uid, phone = user.id, user.phone
            saveUser(uid, yyuser['name'], phone, yyid)
            return yyuser


def getName():
    """获取当前的用户名"""
    user = getUser()
    if not user:
        return False
    else:
        return user['name']


def getPhone():
    """获取手机,会自动尝试同步更新用户手机号"""
    user = getUser()
    if not user:  # 未登录
        return False
    elif user['call']:  # 已经有手机号
        return user['call']
    else:  # 本地无手机号，尝试远端获取
        phone = user['yyid'] and yy.getPhone(user['yyid'])
        _checkPhone(user['id'], phone)
        return phone

        # 逻辑太复杂---删
        # def getPhone():
        #     """获取手机,会自动尝试同步更新用户手机号"""
        #     user = cookie.get('u')
        #     if user:  # 有cookie
        #         if user['call']:  # cookie中有手机号直接返回
        #             return user['call']
        #         elif user['yyid']:  # 尝试获取云印的手机
        #             phone = yy.getPhone(user['yyid'])
        #             if phone:  # 获取到手机号保存并更新
        #                 userModel.save(user['id'], phone=phone)
        #                 user['call'] = phone
        #                 cookie.set('u', user)
        #                 return phone
        #     else:  # 无cookie
        #         yyuser = yy.getUser()  # 云印用户
        #         if not yyuser:
        #             return None
        #         else:
        #             yyid = yyuser['id']
        #             user = userModel.find(_field='id,phone', yyid=yyid)
        #             if not user:  # 数据库无当前用户
        #                 detail = yy.getDetail(yyid)
        #                 phone = detail['phone'] and yy.getPhone(yyid)
        #                 uid = userModel.add(yyid=yyuser['id'], name=yyuser['name'], phone=phone, number=detail['number'], school=yyuser['sch_id'])
        #             elif not user.phone:  # 有用户，无手机号
        #                 uid = user.id
        #                 phone = yy.getPhone(yyid)
        #                 if phone:  # 云印数据获取成功
        #                     userModel.save(uid, phone=phone)
        #             else:  # 本地数据库有手机号
        #                 uid, phone = user.id, user.phone
        #             saveUser(uid, yyuser['name'], phone, yyid)
        #             return phone


def savePhone(phone):
    """保存手机"""
    user = getUser()
    if not user:  # 未登录
        return False
    else:
        user['call'] = phone
        _checkPhone(user['id'], phone)
        return cookie.set('u', user)
