#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：请求服务，目前只支持带token的请求

import requests
import traceback
import core.mylog as log
import os

logging = log.track_log()

result = ''
results = ''

response_result = {
    "status_result": None,
    "status_code": None
}

timeout_Result= {
        "code": -1,
        "message": "请求超时",
        "result": None,
        "run_time": 20000.000
    }


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
        if method.upper() == "POST":
            result = requests.post(url, data, headers=headers)
        if method.upper() == "GET":
            result = requests.get(url, headers=headers)
        response = result.json()
        return response
    except Exception as e:
        logging.error("请求失败%s" % e)
        traceback.print_exc(file=open(os.getcwd()+'/log/error.log', 'w+'))


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
        if method.upper() == "POST":
            result = requests.post(url, data, headers=headers, timeout=3)
        if method.upper() == "GET":
            result = requests.get(url, data, headers=headers, timeout=3)
        if method.upper() == "PUT":
            result = requests.put(url, data, headers=headers)
        if method.upper() == "PATCH":
            result = requests.patch(url, data, headers=headers)
        if method.upper() == "OPTIONS":
            result = requests.options(url, headers=headers)
        run_time = result.elapsed.total_seconds()
        response_code = result.status_code
        if response_code > 200:
            response_result['status_code'] = response_code
            response_result['status_result'] = result.text
            response_result['run_time'] = round(run_time * 1000, 3)
            return response_result
        elif response_code == 200 and result is None:
            return result
        response = result.json()
        response['run_time'] = round(run_time * 1000, 3)
        return response
    except requests.ReadTimeout:
        traceback.print_exc(file=open(os.getcwd()+'/log/error.log', 'a+'))
        return timeout_Result
    except Exception as e:
        logging.error("请求发生异常\n %s" % e)
        traceback.print_exc(file=open(os.getcwd()+'/log/error.log', 'a+'))


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
        traceback.print_exc(file=open(os.getcwd()+'/log/error.log', 'a+'))

