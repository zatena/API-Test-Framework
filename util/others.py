#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 其他公用方法

from __future__ import division
import datetime
import os

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
