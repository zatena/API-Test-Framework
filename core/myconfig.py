#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：配置服务

import configparser

config = configparser.RawConfigParser()


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
        print("获取配置文件失败，%s" % e)


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
        print("获取参数失败，%s" % e)


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
        print("获取title list，%s" % e)


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
        print("获取key list，%s" % e)





