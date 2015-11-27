#-*- coding: UTF-8 -*-
import base64
import datetime
import urllib2
import hashlib

HOST = "https://api.ucpaas.com"
SOFTVER = "2014-06-30"


def getSig(accountSid, accountToken, timestamp):  # 返回签名
    sig = accountSid + accountToken + timestamp
    return hashlib.md5(sig).hexdigest().upper()


def getAuth(accountSid, timestamp):  # 生成授权信息
    src = accountSid + ":" + timestamp
    return base64.encodestring(src).strip()


def request(req, url, accountSid, timestamp, body):  # 生成HTTP报文
    req.add_header("Authorization", getAuth(accountSid, timestamp))
    req.add_header("Accept", "application/json;charset=utf-8")
    req.add_header("Content-Type", "application/json;charset=utf-8")
    if body:
        req.add_header("Content-Length", len(body))
        req.add_data(body)
    try:
        res = urllib2.urlopen(req)
        data = res.read()
        res.close()
    except urllib2.HTTPError, error:
        data = error.read()
        error.close()
    return data


def templateSMS(accountSid, accountToken, appId, toNumbers, templateId, param):
    """
    短信验证码（模板短信）
    toNumber 被叫的号码
    templateId 模板Id
    param <可选> 内容数据，用于替换模板中{数字}
    """
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    signature = getSig(accountSid, accountToken, timestamp)
    url = HOST + "/" + SOFTVER + "/Accounts/" + accountSid + "/Messages/templateSMS?sig=" + signature
    body = '{"templateSMS":{ "appId":"%s","to":"%s","templateId":"%s","param":"%s"}}' % (appId, toNumbers, templateId, param)
    req = urllib2.Request(url)
    body = body.encode('utf-8')
    return request(req, url, accountSid, timestamp, body)
