#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：响应处理服务

import core.mylog as log

logging = log.track_log()


class getRelyValues:

    def get_dict(dict1, values):
        """
        获取请求数据
        :param dic1: 存储数据
        :param values: 指定的关键字
        :return: 指定关键字的值
        """
        global values1, va
        values1 = values
        # 把字典的key和values变成数组
        for k, v in dict1.items():
            if k == values:
                va = v

            # 判断类型是不是list
            elif list is type(v):
                getRelyValues.get_list(v)

            elif type(v) is dict:
                getRelyValues.get_dict(v, values1)

            else:
                # print(str(k) + ":----" + str(v))
                pass

        return va

    def get_list(list1):

        for i in list1:
            if list is type(i):
                getRelyValues.getlget_listsit(i)

            elif dict is type(i):
                getRelyValues.get_dict(i, values1)
            else:
                pass



