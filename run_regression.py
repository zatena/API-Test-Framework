#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 执行包：run regression cases begin with "tezign*.json"

import os
import constants as cs
import util.common as common
import re
import core.myemail as email

reportFile = cs.REPORT_PATH

ProRegTest = common.ProProjectRegression()


casePath = os.getcwd()+'/case'
dirs = os.listdir(casePath)
report = None

for i in dirs:
    if re.match("tezign_*", i):
        caseFile = os.path.join(casePath, i)

        """1. 执行测试用例
           2. 生成测试报告
           3. 发送报告邮件
        """
        report = ProRegTest.build_report_regression(caseFile)

email.email(report)


# casePath = os.getcwd()+'/case/tez_proregression.json'
# ProRegTest.build_report_regression(casePath)





