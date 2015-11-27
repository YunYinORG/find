#!/usr/bin/env python
# coding=utf-8
from config import VIEW_BASE as BASE_URL
__doc__ = "短链接管理"


def create(find_id, lost_id):
    """创建快速找回URL"""
    head = str(lost_id) + hex(int(find_id))[1:]
    import uuid
    s = uuid.uuid1().__str__().replace('-', '')
    token = head + s[0:(32 - len(head))]
    return token, BASE_URL + token


def short(url):
    """创建短链接"""
    return url[7:22]
