#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 执行包：run regression cases begin with "tezign*.json"

import os
import constants as cs
import util.common as common
import re

reportFile = cs.REPORT_PATH

ProRegTest = common.ProProjectRegression()

# casePath = os.getcwd()+'/case/tezign_designergroup.json'
casePath = os.getcwd()+'/case'

dirs = os.listdir(casePath)

for i in dirs:
    if re.match("tezign_*", i):
        caseFile = os.path.join(casePath, i)

        """1. 执行测试用例生成测试报告"""
        ProRegTest.build_report_regression(caseFile)

        """3. 发送测试报告"""
        # ProRegTest.send_email_regression(reportFile)










