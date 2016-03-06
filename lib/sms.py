#!/usr/bin/env python
# coding=utf-8
from ucpass import templateSMS
from json import loads
from random import randint
import config


def _sendSms(to, templateId, param):  # 发送短信
    result = templateSMS(config.SMS_ACCOUNT, config.SMS_TOKEN, config.SMS_APPID, to, templateId, param)
    if not result:
        return False
    try:
        result = loads(result)
        return result["resp"]["respCode"] == "000000"
    except Exception:
        return None


def sendLogin(to):
    """临时登录验证"""
    code = str(randint(1000, 999999))
    param = "%s,3" % (code)
    return _sendSms(to, config.SMS_LOGIN, param) and code


def sendBind(to):
    """绑定手机"""
    code = str(randint(1000, 999999))
    param = "%s,3" % (code)
    return _sendSms(to, config.SMS_BIND, param) and code


def sendNotify(to, finder, finder_phone, site='http://find.yunyin.org', thing="校园卡"):
    """发送通知"""
    param = "%s,%s,%s,%s" % (thing, finder, finder_phone, site+' ')
    return _sendSms(to, config.SMS_NOTIFY, param)


def sendResult(to, status):
    """发送结果，感谢或者举报警告"""
    return None
