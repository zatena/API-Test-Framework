#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：配置服务

import configparser
import jsonpath
import json
import core.mylog as log

logging = log.track_log()
config = configparser.RawConfigParser()


def get_casename(filename):
    """
    获取用例文件
    :param filename: 用例文件
    :return: 用例名，数据字典
    """
    f = open(filename, encoding='utf-8')
    dic = json.load(f)
    names = jsonpath.jsonpath(dic,'$..caseName')
    return names, dic

def get_casedata(filename):
    """
    获取请求数据
    :param filename: 用例文件
    :return: 请求地址，方法，数据，请求头
    """
    f = open(filename, encoding='utf-8')
    data = json.load(f)
    url = jsonpath.jsonpath(data,'$..caseUrl')
    method = jsonpath.jsonpath(data,'$..caseMethod')
    data = jsonpath.jsonpath(data,'$..body')
    headers = jsonpath.jsonpath(data,'$..headers')
    return url, method, data, headers

def get_config(filename):
    """
    读配置文件
    :param filename: 配置文件名
    :return: None
    """
    global config
    try:
        config.read(filename)
        return True
    except Exception as e:
        logging.error("获取配置文件失败，%s" % e)


def get_data(title, key):
    """
    参数配置
    :param title: 配置文件的头信息
    :param key: 配置文件的key值
    :return: 配置文件的value
    """
    try:
        value = config.get(title,key)
        return value
    except Exception as e:
        logging.error("获取参数失败，%s" % e)


def get_title_list():
    """
    参数配置
    获取所有title
    .decode('string_escape')去掉转义字符，输出中文字符
    :return: title list
    """
    try:
        title = config.sections()
        return str(title).encode("utf-8").decode("utf-8")
    except Exception as e:
        logging.error("获取title list，%s" % e)


def get_key_list():
    """
    参数配置
    获取所有key
    :return: key list
    """
    try:
        key_list = config.options()
        return str(key_list)
    except Exception as e:
        logging.error("获取key list，%s" % e)





