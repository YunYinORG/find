#!/usr/bin/env python
# coding=utf-8
import web
from json import dumps


def json(status, message=None):
    """以json格式返回数据"""
    data = {'status': status, 'message': message}
    web.header('Content-Type', 'application/json;charset=utf-8')
    return dumps(data, ensure_ascii=False, encoding='utf-8')
