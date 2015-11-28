#!/usr/bin/env python
# coding=utf-8

from db import Model, db
"""todo : 临时账号和云印账号数据合并"""
__doc__ = "用户数据库层封装"
_table = 'user'
userModel = Model(_table)


def merge(phone_id, card_id):
    """手机临时账号和校园卡账号合并"""
    record_table = 'record'
    t = db.transaction()
    phone_id, card_id = int(phone_id), int(card_id)
    try:
        # 转移记录
        db.update(record_table, where="last_id=%i" % phone_id, last_id=card_id)
        db.update(record_table, where="find_id=%i" % phone_id, find_id=card_id)
        # 删除合并用户
        phone_user = db.select(_table, where="id=%i" % phone_id, limit=1, what='phone')
        try:
            db.delete(_table, where="id=%i" % phone_id)
        except:
            db.update(_table, where="id=%i" % phone_id, phone=None)
        db.update(_table, where="id=%i" % card_id, phone=phone_user[0].phone)
    except:
        t.rollback()
        return False
    else:
        t.commit()
        return card_id
