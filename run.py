#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 执行包：run single api case

import util.common as common
import constants as cs
import os


reportFile = cs.REPORT_PATH

ApiTest = common.ApiTest()

caseFile = os.getcwd()+'/case/aa.json'

"""1. 执行测试用例"""
# ApiTest.execute_case(caseFile)

"""2. 生成测试报告"""
ApiTest.build_report(caseFile)

"""3. 发送测试报告"""
# ApiTest.send_email(reportFile)



