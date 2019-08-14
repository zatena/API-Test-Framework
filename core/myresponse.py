#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：响应处理服务

import core.mylog as log

logging = log.track_log()


class getRelyValues:
    def __init__(self):
        pass

    def get_dict_value(self, dict_data, values, index, dict_list):
        result_list = self.get_dict(dict_data, values, index, dict_list)

        if len(result_list) == 0:
            logging.warn("依赖接口没返回值")
            return

        result = result_list[int(index) - 1]
        dict_list.clear()
        return result

    def get_dict(dict_data, values, index, dict_list):
        """
        获取请求数据
        :param dict_data: 存储数据
        :param values: 关键字
        :param index: 关键字的顺序
        :return: 关键字的值
        """
        global values1, va
        values1 = values

        # 把字典的key和values变成数组
        for k, v in dict_data.items():
            if k == values:
                va = v
                dict_list.append(va)
                continue

            # 判断类型是不是list
            elif list is type(v):
                getRelyValues.get_list(v, index, dict_list)

            elif type(v) is dict:
                getRelyValues.get_dict(v, values1, index, dict_list)

            else:
                # print(str(k) + ":----" + str(v))
                pass

        return dict_list

    def get_list(list1, index, dict_list):

        for i in list1:
            if list is type(i):
                getRelyValues.get_list(i, index, dict_list)

            elif dict is type(i):
                getRelyValues.get_dict(i, values1, index, dict_list)
            else:
                pass



