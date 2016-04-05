#!/usr/bin/env python
# coding=utf-8
import cookie
import yunyin as yy
from model.user import merge, userModel


def _checkPhone(user, phone):
    """检查手机号是否重复"""
    phone_user = userModel.find('id,yyid', phone=phone)
    if not phone_user:  # 手机号未登录过
        return userModel.save(user['id'], phone=phone)
    elif phone_user.id == user['id']:  # 同一个账号
        return True
    elif not phone_user.yyid:  # 临时登录过
        return merge(phone_user.id, user['id'])
    elif phone_user.yyid != user['yyid']:  # 异常情况,此手机已经绑定了其他账号
        return False


def saveUser(uid, name, phone=None, yyid=None):
    """保存用户信息"""
    user = {'id': uid, 'name': name, 'yyid': yyid, 'call': phone}
    cookie.set('u', user)
    return user


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
            # 检查账号同步情况
            yyid = int(yyuser['id'])
            sync_user = userModel.find(_field='id,phone', yyid=yyid)
            if sync_user:
                # yyid已经同步
                if sync_user.phone:  # 已经同步了手机
                    phone = sync_user.phone
                else:  # 未同步的手机
                    phone = yy.getPhone(yyid)
                    if phone:
                        # 手机号未同步
                        phone_user = userModel.find('id', phone=phone)  # 云印账号带有手机
                        if not phone_user:
                            # 此手机号未曾使用直接使用
                            userModel.save(uid, phone=phone)
                        else:
                            # 使用过，合并账号
                            uid = merge(phone_user.id, sync_user.id)
                return saveUser(sync_user.id, yyuser['name'], phone, yyid)

            # 未同步账户
            # 查询该学号的用户
            user = userModel.find(_field='id,phone,yyid,type',number=yyuser['number'], school=int(yyuser['sch_id']))
            # 查询绑定该手机的用户
            phone = yy.getPhone(yyid)
            phone_user = phone and userModel.find('id,yyid', phone=phone)  # 云印账号带有手机

            if not (user or phone_user):
                # 手机和学号都不存在
                # 直接写入数据库
                uid = userModel.add(yyid=yyid, name=yyuser['name'], phone=phone, number=yyuser['number'], school=yyuser['sch_id'], type=1)
            elif user and not phone_user:
                # 学号已存在，手机未使用过
                # 更新用户信息
                uid = user.id
                userModel.save(uid, yyid=yyid, name=yyuser['name'], phone=phone, type=1)
            elif not user and phone_user:
                # 学号不存在，手机使用过【临时登录】
                # 更新临时账号
                uid = phone_user.id
                userModel.save(uid, yyid=yyid, name=yyuser['name'], number=yyuser['number'], school=yyuser['sch_id'], type=1)
            else:
                # 两个都存在
                # 合并账号
                uid = merge(phone_user.id, user.id)
                userModel.save(uid,yyid=yyid,type=1)
            return saveUser(uid, yyuser['name'], phone, yyid)


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
        _checkPhone(user, phone)
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
        _checkPhone(user, phone)
        return cookie.set('u', user)
