#!/usr/bin/env python
# coding=utf-8
import re
from config import REGX_SHOOL

_regex_phone = '^1[34578]\d{9}$'
_regex_name = ur'^[\u4E00-\u9FA5]{2,5}(·[\u4E00-\u9FA5]{2,8})?$'


def phone(number):
    """手机号格式验证"""
    return number and (re.match(_regex_phone, str(number)) != None)


def name(string):
    """姓名验证"""
    return string and (re.match(_regex_name, string.decode('utf-8')) != None)


def card(number):
    """卡号验证"""
    return number and (re.match(REGX_SHOOL[0], str(number)) != None)


def school(number):
    """根据学号判断学校，返回对应ID"""
    for sch_id, regx in enumerate(REGX_SHOOL[1:], 1):
        if re.match(regx, number):
            return sch_id
    return 0
