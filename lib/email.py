# #!/usr/bin/env python
# # coding=utf-8
# import config
# import web

# web.config.smtp_server = config.MAIL_SMTP
# web.config.smtp_port = config.MAIL_PORT
# web.config.smtp_username = config.MAIL_USER
# web.config.smtp_password = config.MAIL_PWD
# web.config.smtp_starttls = True


# def sendMail(to, content):  # 发送邮件
#     subject = '测试邮件'
#     headers = {'Content-Type': 'text/html;charset=utf-8'}
#     return web.sendmail(config.MAIL_USER, to, subject, content, headers=headers)