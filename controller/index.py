#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user
"""首页[done]"""

class index:

    """首页"""

    def GET(self):
        html = web.template.frender('templates/index.html')
        name = user.getName()
        return html(name)
