#!/usr/bin/env python
# coding=utf-8
from ucpass import templateSMS
from json import loads
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


def sendBind(to, code):
    param = "%s,3" % (code)
    return _sendSms(to, config.SMS_BIND, param)


def sendNotify(to, msg):
    pass


def sendLogin(to, msg):
    pass
