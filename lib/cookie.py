#!/usr/bin/env python
# coding=utf-8
import web
import base64
from config import COOKIE_KEY
from json import dumps, loads
from Crypto.Cipher import AES

__doc__ = "加密cookie存取"
_cipher = AES.new(COOKIE_KEY)


def _encrypt(data):
    text = dumps(data, ensure_ascii=False, encoding='utf8')
    text = text.encode('utf-8')
    text += b"\0" * (AES.block_size - len(text) % AES.block_size)  # ('\0'*(16-len(text) % 16))
    e = _cipher.encrypt(text)
    return base64.urlsafe_b64encode(e).rstrip('=')


def _decrypt(text):
    try:
        text += (b'='*(4-len(text) % 4))
        m = base64.urlsafe_b64decode(text)
        s = _cipher.decrypt(m).rstrip('\0')
        return loads(s)
    except Exception:
        return None


def set(name, value):
    """保存加密的cookie"""
    web.setcookie(name, _encrypt(value), path='/', httponly=1)


def get(name):
    """ 获取cookie,空或者无效返回None"""
    value = web.cookies().get(name)
    return value and _decrypt(value)


def delete(name):
    web.setcookie(name, None, -1, path='/', httponly=1)
