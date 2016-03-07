#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user

class nku(object):
    """南开"""
    def GET(self):
    	userinfo=user.getUser()
    	render  = web.template.render ('templates/school/',base="layout")
    	if userinfo:
    		return render.nku(userinfo)
    	else:
    		return render.nku_unlogin()