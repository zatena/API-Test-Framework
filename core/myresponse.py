#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：响应处理服务

import core.mylog as log

logging = log.track_log()


class getRelyValues:



    def get_dict(dict1, values, index,dictList):
        """
        获取请求数据
        :param dic1: 存储数据
        :param values: 关键字
        :param index: 关键字的顺序
        :return: 关键字的值
        """
        global values1, va
        values1 = values
        # 把字典的key和values变成数组

        for k, v in dict1.items():
            if k == values:
                va = v
                dictList.append(va)
                continue

            # 判断类型是不是list
            elif list is type(v):
                getRelyValues.get_list(v,index,dictList)

            elif type(v) is dict:
                getRelyValues.get_dict(v, values1,index,dictList)

            else:
                # print(str(k) + ":----" + str(v))
                pass


        return dictList[index-1]

    def get_list(list1,index,dictList):

        for i in list1:
            if list is type(i):
                getRelyValues.get_list(i,index,dictList)

            elif dict is type(i):
                getRelyValues.get_dict(i, values1,index,dictList)
            else:
                pass



