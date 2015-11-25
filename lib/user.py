#!/usr/bin/env python
# coding=utf-8
import cookie
import yunyin as yy


def saveUser(name, yyid=None, phone=None):
    """保存用户信息"""
    user = {'name': name, 'yyid': yyid}
    if phone:
        user['call'] = phone
    return cookie.set('u', user)


def getUser():
    """获取当前的用户"""
    user = cookie.get('u')
    if user:
        return user
    else:
        yyuser = yy.getUser()
        if not yyuser:
            return None
        else:
            saveUser(user['name'], user['id'])
            return user


def getName():
    """获取当前的用户名"""
    user = getUser()
    if not user:
        return False
    else:
        return user['name']


def getPhone():
    """获取手机"""
    user = getUser()
    if not user:  # 未登录
        return False
    elif user.has_key('call'):  # 信息中不包含手机
        return user['call']
    else:
        phone = yy.getPhone(user['yid'])
        if not phone:
            return None
        else:
            user['call'] = phone
            cookie.set('u', user)
            return phone


def savePhone(phone):
    """保存手机"""
    user = getUser()
    if not user:  # 未登录
        return False
    else:
        user['call'] = phone
        return cookie.set('u', user)
