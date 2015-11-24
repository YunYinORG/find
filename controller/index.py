#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user


class index:

    """首页"""

    def GET(self):
        html = web.template.frender('templates/index.html')
        name = user.getName()
        return html(name)
