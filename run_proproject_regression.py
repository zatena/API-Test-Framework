#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 执行包：run

import util.common as common
import constants as cs
import os


reportFile = cs.REPORT_PATH

ProRegTest = common.ProProjectRegression()

caseFile = os.getcwd()+'/case/proProjectRegression.ini'
"""1. 执行测试用例"""
# ProRegTest.execute_case_proprojectreg(caseFile)

"""2. 生成测试报告"""
ProRegTest.build_report_proprojectreg(caseFile)

"""3. 发送测试报告"""
# ProRegTest.send_email_proprojectreg(reportFile)



