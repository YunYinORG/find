#!/usr/bin/env python
# coding=utf-8
import web
import lib.user as user
from lib.response import json as json
from model import userModel, recordModel
import config
"""招领信息汇总"""

class found(object):
    """docstring for found"""
    def GET(self):
        sch = int(web.input(sch=None).sch)
        # if sch == 1: 

        return sch;