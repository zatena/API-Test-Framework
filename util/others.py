#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 其他公用方法

from __future__ import division
import datetime
import os
import core.mylog as log

logging = log.track_log()
testdata = None

def get_now():
    currenttime = datetime.datetime.now()
    strtime = currenttime.strftime("%Y%m%d %H:%M:%S")
    strtime_ymd = currenttime.strftime("%Y%m%d")
    return currenttime, strtime, strtime_ymd


def get_mills(starttime, endtime):
    delta = (endtime - starttime).seconds
    return delta


def get_micros(starttime, endtime):
    delta = (endtime - starttime).microseconds
    return delta


def get_future(days):
    futuretime = (datetime.datetime.now()+datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    return futuretime


def get_filename(filepath):
    global testdata
    dirs = os.listdir(filepath)
    for file in dirs:
        if file == '.jpg':
            testdata = file
    return testdata

# def result_pass(name, pass_result, request_data, actual_response):
#     logging.info("回归测试通过:%s" % name)
#     test_status = "成功"
#     pass_result = pass_result + 1
#     request_log_message = "输入值:%s\n" % request_data
#     result_log_message = "输出结果:%s\n" % actual_response
#     return(test_status, pass_result, request_log_message, result_log_message)
#
# def result_fail(name, fail_result, request_data, actual_response):
#     logging.info("回归测试失败:%s" % name)
#     test_status = "失败"
#     fail_result = fail_result + 1
#     request_log_message = "输入值:%s\n" % request_data
#     result_log_message = "输出结果:%s\n" % actual_response
#     return(test_status, fail_result, request_log_message, result_log_message)

