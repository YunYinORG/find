#!/usr/bin/env python
# coding=utf-8

from web import database, db as webdb
from config import DB_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PWD

__doc__ = "数据库连接"
db = database(dbn=DB_TYPE, host=DB_HOST, port=DB_PORT, db=DB_NAME, user=DB_USER, pw=DB_PWD)


def buildWhere(where_dict, grouping="AND"):
    return webdb.sqlwhere(where_dict, grouping=grouping)


class Model(object):

    """数据库Model"""

    def __init__(self, table):
        self._table = table

    def find(self, uid=None, _field='*', **kwargs):
        """单个查询记录"""
        if uid and (isinstance(uid, int) or uid.isalnum()):
            kwargs["id"] = int(uid)
        elif isinstance(uid, str):
            _field = uid
        else:
            return None
        where = buildWhere(kwargs)
        result = db.select(self._table, where=where, limit=1, what=_field)
        if len(result) > 0:
            return result[0]

    def select(self, _field='*', limit=10, offset=0, order=None, **kwargs):
        """批量查询"""
        more = {}
        if limit:
            more['limit'] = limit
        if offset:
            more['offset'] = offset
        if order:
            more['order'] = order
        if kwargs:
            where = buildWhere(kwargs)
            result = db.select(self._table, where=where, what=_field, **more)
        else:
            result = db.select(self._table, what=_field, **more)
        if len(result) > 0:
            return result.list()
        else:
            return None

    def save(self, uid, **kwargs):
        """更新数据"""
        where = "id=%i" % int(uid)
        return db.update(self._table, where=where, **kwargs)

    def add(self, data=None, **kwargs):
        """"添加用户"""
        if type(data) == 'dict':
            kwargs = data
        return kwargs and db.insert(self._table, **kwargs)

    def delete(self, uid):
        where = "id=%i" % int(uid)
        """"删除用户,如果不能删除状态设为 1"""
        if db.delete(self._table, where=where):
            return True
        else:
            return db.update(self._table, where=where, status=0)
