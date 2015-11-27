#!/usr/bin/env python
# coding=utf-8
import cookie
import yunyin as yy
from model.user import userModel


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
            user = userModel.find(_field='id,phone', yyid=yyid)
            if not user:  # 数据库未同步
                detail = yy.getDetail(yyid)
                phone = detail['phone'] and yy.getPhone(yyid)
                uid = userModel.add(yyid=yyuser['id'], name=yyuser['name'], phone=phone, number=detail['number'], school=yyuser['sch_id'])
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
    user = cookie.get('u')
    if user:  # 有cookie
        if user['call']:  # cookie中有手机号直接返回
            return user['call']
        elif user['yyid']:  # 尝试获取云印的手机
            phone = yy.getPhone(user['yyid'])
            if phone:  # 获取到手机号保存并更新
                userModel.save(user['id'], phone=phone)
                user['call'] = phone
                cookie.set('u', user)
                return phone
    else:  # 无cookie
        yyuser = yy.getUser()  # 云印用户
        if not yyuser:
            return None
        else:
            yyid = yyuser['id']
            user = userModel.find(_field='id,phone', yyid=yyid)
            if not user:  # 数据库无当前用户
                detail = yy.getDetail(yyid)
                phone = detail['phone'] and yy.getPhone(yyid)
                uid = userModel.add(yyid=yyuser['id'], name=yyuser['name'], phone=phone, number=detail['number'], school=yyuser['sch_id'])
            elif not user.phone:  # 有用户，无手机号
                uid = user.id
                phone = yy.getPhone(yyid)
                if phone:  # 云印数据获取成功
                    userModel.save(uid, phone=phone)
            else:  # 本地数据库有手机号
                uid, phone = user.id, user.phone
            saveUser(uid, yyuser['name'], phone, yyid)
            return phone


def savePhone(phone):
    """保存手机"""
    user = getUser()
    if not user:  # 未登录
        return False
    else:
        user['call'] = phone
        userModel.save(user['id'], phone=phone)
        return cookie.set('u', user)
