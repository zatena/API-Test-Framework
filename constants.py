#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 通用包：常量

import os
import importlib, sys
importlib.reload(sys)
import time
import random
import string

BASEURL = "http://47.93.82.56:8080"

REPORT_PATH = os.getcwd()+'/report'

DELIVERY_PATH = os.getcwd()+'/data'

CASE_PATH = os.getcwd()+'/case/项目状态扩展优化.ini'

REPORT_TITLE = "接口自动化测试报告" + time.strftime('%Y%m%d',time.localtime(time.time()))
PRO_REPORT_TITLE = "企业项目流程回归测试"
COMMON_REPORT_TITLE = "普通项目流程回归测试"

# 测试结果常量


# 测试用例常量
METHOD = 'method'
URL = 'url'
DATA = 'data'
NAME = 'name'
NUMBER = 'number'
CODE = 'code'
HEADERS = 'headers'
VPROJECT_ID = 2927


# 邮件常量
MAIL_HOST = 'smtp2525.sendcloud.net'
MAIL_USER = 'tezign_send'
MAIL_PASS = 'hhIksYtHPnH2l7dj'

MAIL_SENDER = 'zhengjingjing@tezign.com'
MAIL_RECEIVER = 'zhengjingjing@tezign.com'
SUBJECT = '接口自动化测试报告'

# 数据库常量
DB_HOST = '123.57.137.216'
DB_USER = 'test'
DB_PASSWORD = 'tezign'
DB_NAME = 'tezign_uat'


