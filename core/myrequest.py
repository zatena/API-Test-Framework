#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：请求服务，目前只支持带token的请求

import requests
import core.mylog as log

logging = log.track_log()
result = ''
results = ''

def api(method, url, data, headers):
    """
    定义一个请求接口的方法和参数
    :param method: 请求类型
    :param url: 请求地址
    :param data: 请求参数
    :param headers: 请求头信息
    :return: code码
    """
    global result

    try:
        if method == ('post' or "POST"):
            result = requests.post(url, data, headers=headers)
        if method == ('get' or 'GET'):
            result = requests.get(url, data, headers=headers)

        response = result.json()
        code = response.get('code')
        return code
    except Exception as e:
        logging.error("请求失败%s" % e)


def get_message(method, url, data, headers):
    """
    定义一个请求接口的方法和参数
    :param method: 请求类型
    :param url: 请求地址
    :param data: 请求参数
    :param headers: 请求头信息
    :return: message信息
    """
    global result, results

    try:
        if method == ('post' or 'POST'):
            result = requests.post(url, data, headers=headers, timeout=3)
        if method == ('get' or 'GET'):
            result = requests.get(url, data, headers=headers, timeout=3)
        if method == ('put' or 'PUT'):
            result = requests.put(url, data, headers=headers)
        if method == ('patch' or 'PATCH'):
            result = requests.patch(url, data, headers=headers)
        if method == ('options' or 'OPTIONS'):
            result = requests.options(url, headers=headers)

        run_time = result.elapsed.total_seconds()
        response = result.json()
        code = response.get('code')
        if code == 500:
            results = None
        elif code == 0:
            results = response.get('result')
        else:
            results = response.get('result')
        message = response.get('message')
        content = {'code': code, 'message': message, 'result': results, 'run_time':run_time}
        return content
    except Exception as e:
        logging.error("请求失败%s" % e)


def get_mfd(method, url, data, headers):
    """
    定义一个请求multipart/form-data接口的方法和参数
    :param url: 请求地址
    :param method: 请求方法
    :param data: 请求文件
    :param headers: 请求头信息
    :return: result信息
    """
    global result
    try:
        if method == ('post' or 'POST'):
            result = requests.post(url, data=data, headers=headers)
        response = result.json()
        return response
    except Exception as e:
        logging.error("请求失败%s" % e)





