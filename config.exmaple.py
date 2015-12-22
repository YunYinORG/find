#!/usr/bin/env python
# coding=utf-8

# 数据库信息
DB_TYPE = 'mysql'
try:
    import sae.const
    IS_SAE = True
    DB_NAME = sae.const.MYSQL_DB      # 数据库名
    DB_USER = sae.const.MYSQL_USER    # 用户名
    DB_PWD = sae.const.MYSQL_PASS    # 密码
    DB_HOST = sae.const.MYSQL_HOST    # 主库域名（可读写）
    DB_PORT = int(sae.const.MYSQL_PORT)    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
    # sae.const.MYSQL_HOST_S
except Exception:
    IS_SAE = False
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_NAME = 'yunyinfind'
    DB_PORT = 3306
    DB_PWD = ''

# 云印接口
YUNYIN_KEY = "yunyincard"
YUNYIN_API = "http://api.yunyin.org/"

#微博接口
WEIBO_KEY=2681865267
WEIBO_SECRET='f92c633f332d26009bc71c6bb269683e'
WEIBO_CALLBACK='http://2.newfuturepy.sinaapp.com/weibo/callback'
WEIBO_ACCOUNT='xxxxxx'
WEIBO_PWD='xxxxxx'


# 邮件
MAIL_SMTP = 'smtp.exmail.qq.com'
MAIL_PORT = 465
MAIL_USER = 'test@mail.yunyin.org'
MAIL_PWD = ''

# 短信
SMS_ACCOUNT = ''
SMS_APPID = ''
SMS_TOKEN = ''
SMS_NOTIFY = ''
SMS_LOGIN = ''
SMS_BIND = ''

# cookie加密
COOKIE_KEY = 'qhsdfsffffffffff75V4d7F-sdfsf.wN'

# 学校正则
REGX_SHOOL = (
    '^(\d{7}|\d{10})$',  # 通用正则
    '^(([1][0-5]\d{5})|([1|2]1201[0-5]\d{4}))$',  # 南开
    '^[1-4]01[0-5]\d{6}$',  # 天大
    '^((0[1-5][01][0-9])|(1[139][05][1-4]))1[2-5]\d{4}$'  # 天商职
)

#快速查看地址
VIEW_BASE="http://find.yunyin.org/record/v/"

