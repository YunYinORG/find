#!/usr/bin/env python
# coding=utf-8
import web
import base64
import json
import config
from Crypto.Cipher import AES

__doc__ = "加密cookie存取"
_cipher = AES.new(config.COOKIE_KEY)


def _encrypt(data):
    text = json.dumps(data, ensure_ascii=False, encoding='utf-8')
    text += ('\0'*(16-len(text) % 16))
    e = _cipher.encrypt(text)
    return base64.urlsafe_b64encode(e).rstrip('=')


def _decrypt(text):
    try:
        text += ('='*(3-len(text) % 3))
        m = base64.urlsafe_b64decode(text)
        s = _cipher.decrypt(m).rstrip('\0')
        return json.loads(s)
    except Exception:
        return None


def set(name, value):
    """保持加密的cookie"""
    web.setcookie(name, _encrypt(value), path='/', httponly=1)


def get(name):
    """ 获取cookie,空或者无效返回None"""
    value = web.cookies().get(name)
    if value:
        return _decrypt(value)
    else:
        return None


def delete(name):
    web.setcookie(name, None, -1, path='/', httponly=1)
