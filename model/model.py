#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 报告对象

"""
测试报告模板的对象
"""


class ReportModel:
    sum_report = []
    name = ''
    all_test = 0
    pass_test = 0
    fail_test = 0
    skip_test = 0
    total_run_time = ''

    def __init__(self, sum_report, name, all_test, pass_test, fail_test, skip_test, total_run_time):
        self.sum_report = sum_report
        self.name = name
        self.all_test = all_test
        self.pass_test = pass_test
        self.fail_test = fail_test
        self.skip_test = skip_test
        self.total_run_time = total_run_time