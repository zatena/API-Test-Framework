#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：日志服务


import logging

"""日志级别分别为：DEBUG,INFO,WARNING,ERROR,CRITICAL"""


def track_log():
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = "%m/%d/%Y %H:%M:%S %a %p"
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format)
    return logging


