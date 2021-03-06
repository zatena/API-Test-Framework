#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 主要公用方法

import datetime
import json
import time
import os
import random
import string
import constants as cs
import core.myconfig as rc
import core.myemail as email
import core.myrequest as request
import model.model as mm
import model.report as mr
import util.others as others
import re

from core.myresponse import getRelyValues
import traceback
import core.mylog as log

logging = log.track_log()

summary_report = []
single_start = datetime.datetime.now()
single_end = datetime.datetime.now()
content = None
code = None
message = None
result = None
delivery_name = others.get_filename(cs.DELIVERY_PATH)
collect_data = {}
pass_result = 0
fail_result = 0
skip_result = 0
dict_list = []
case_all_count = 0


class MyRegression:

    excReport = mr.Report()
    getRelyValues = getRelyValues()

    def __init__(self):
        pass

    def execute_case(self, filename):
        """
        :param filename: 用例文件名称
        :return: 测试结果的报告模板

        """
        global summary_report, message, result, code, pass_result, fail_result, skip_result, case_all_count

        report_title = cs.TEST_REPORT_TITLE
        case_names = rc.get_casename(filename)[0]
        case_lists = rc.get_casename(filename)[1]
        all_result = len(case_names)
        case_all_count = all_result + case_all_count
        total_start = others.get_now()[0]
        project_name = "企业测试项目" + ''.join(random.sample(string.ascii_letters + string.digits, 3))
        delivery_time = str(others.get_future(60))
        caseScenario = case_lists['scenarioName']

        try:
            for i in range(0, all_result):
                case_list = case_lists['steps'][i]
                name = case_names[i]
                method = case_list['caseMethod']
                request_data = case_list['request']
                expect_body = case_list['assertions']['body']
                expect_code = expect_body['code']
                expect_assert = None
                if len(expect_body) == 2:
                    expect_assert = expect_body['assert']
                assert_len = 0
                if case_list['caseName'] == '发布企业项目':
                    case_list['request']['body']['projectName'] = project_name
                if case_list['caseName'] == '发布企业项目':
                    case_list['request']['body']['deliveryTime'] = delivery_time
                if case_list['caseName'] == '提交确认函':
                    case_list['request']['body']['projectName'] = project_name + '子项目'
                str_data = str(case_list)
                if len(collect_data) > 0:
                    match_object = re.findall('.*?([\u4E00-\u9FA5]+\.[\d]\.[\\w]+)', str_data)
                    expect_assert_name = str(expect_assert).split(":")[0]
                    if expect_assert_name in match_object:
                        match_object.remove(expect_assert_name)
                    if len(match_object) == 0:
                        pass
                    else:
                        for i in match_object:
                            collect_response = collect_data[i.split('.')[0]]
                            res_code = getRelyValues.get_dict_value(getRelyValues, collect_response, 'code', 1, dict_list)
                            if int(res_code) > 0:
                                continue

                            value_index = i.split('.')[1]
                            actual_value = i.split('.')[2]
                            replace_value = getRelyValues.get_dict_value(getRelyValues, collect_response, actual_value,
                                                                         int(value_index), dict_list)

                            str_data = str_data.replace(i, str(replace_value))
                            data_json = eval(str_data)
                            headers = data_json['request']['headers']
                            api_url = data_json['caseUrl']
                            url = cs.BASEURL + api_url
                            _data = data_json['request']['body']

                data_json = eval(str_data)
                headers = data_json['request']['headers']
                api_url = data_json['caseUrl']
                url = cs.BASEURL + api_url
                _data = data_json['request']['body']
                data = json.dumps(_data, indent=4, sort_keys=False, ensure_ascii=False)
                data = data.encode('utf-8')
                if 'caseSleep' in data_json:
                    sleep_time = data_json['caseSleep']
                    actual_response = request.get_message(method, url, data, headers)
                    time.sleep(sleep_time)
                else:
                    actual_response = request.get_message(method, url, data, headers)
                collect_data[name] = actual_response
                res_str = ""
                if expect_assert is not None:
                    assert_object = re.findall('.*?([\u4E00-\u9FA5]+\.[\d]\.[\\w]+)', expect_assert)
                    for k in assert_object:
                        res_str = k.split('.')[2]
                        res_str_index = k.split('.')[1]
                        assert_replace_value = getRelyValues.get_dict_value(getRelyValues, actual_response, res_str,
                                                                            res_str_index, dict_list)
                        k = expect_assert.replace(k, str(assert_replace_value))
                        assert_list = k.split(":")
                        assert_len = len(set(assert_list))

                try:
                    if actual_response is not None:
                        if 'status_result' in actual_response:
                            actual_code = actual_response['status_result'][0]
                            if actual_code == -1 or -3:
                                actual_status_code = actual_response['status_code']
                            elif actual_code == 1:
                                actual_status_code = actual_code
                            else:
                                actual_status_code = None
                        else:
                            actual_code = actual_response['code']
                            actual_status_code = None

                        if actual_status_code is not None:
                            logging.info("回归测试失败:%s" % name)
                            test_status = "失败"
                            fail_result = fail_result + 1
                            request_log_message = "输入值: %s\n" % request_data

                        elif actual_code == expect_code and expect_assert is None:
                            logging.info("回归测试通过:%s" % name)
                            test_status = "成功"
                            pass_result = pass_result + 1
                            request_log_message = "输入值: %s\n" % request_data

                        elif assert_len == 1:
                            logging.info("回归测试通过:%s" % name)
                            test_status = "成功"
                            pass_result = pass_result + 1
                            request_log_message = "输入值: %s\n" % request_data

                        else:
                            logging.info("回归测试失败:%s" % name)
                            test_status = "失败"
                            fail_result = fail_result + 1
                            if assert_len > 1:
                                actual_result = res_str + "预期结果:%s\n" % assert_list[1] + " 实际结果:%s\n" % assert_list[0]
                                request_log_message = "输入值: %s\n" % request_data
                                result_log_message = "输出结果: 预判值错误, %s\n" % actual_result
                                run_time = str(actual_response['run_time']) + 'ms'
                                summary_report = self.excReport.sum_result(caseScenario, url, method, name, run_time,
                                                                           test_status, request_log_message,
                                                                           result_log_message)
                                continue
                            else:
                                request_log_message = "输入值: %s\n" % request_data

                except Exception as e:
                    logging.error("无返回结果%s" % e)
                    traceback.print_exc(file=open(os.getcwd()+'/log/error.log', 'a+'))
                run_time = str(actual_response['run_time']) + 'ms'
                # del actual_response['run_time']
                result_log_message = "输出结果:%s\n" % actual_response
                if len(url) > 120:
                    url = url[0:110]
                summary_report = self.excReport.sum_result(caseScenario, url, method, name, run_time, test_status,
                                                           request_log_message, result_log_message)

        except Exception as e:
            logging.error(e)
            traceback.print_exc(file=open(os.getcwd()+'/log/error.log', 'a+'))

        total_end = others.get_now()[0]
        total_run_time = str(others.get_mills(total_start, total_end)) + 's'

        skip_result = case_all_count - pass_result - fail_result
        report_model = mm.ReportModel(summary_report, report_title, case_all_count, pass_result,
                                      fail_result, skip_result, total_run_time)

        return report_model

    def build_report(self, filename):
        try:
            test_report = self.execute_case(filename)
            return self.excReport.build_report(test_report.sum_report, test_report.name, test_report.all_test,
                                               test_report.pass_test, test_report.fail_test, test_report.skip_test,
                                               test_report.total_run_time)
        except Exception as e:
            logging.error(e)
            traceback.print_exc(file=open(os.getcwd()+'/log/error.log', 'a+'))

    def send_email(self, reportfile):
        reports = os.listdir(reportfile)
        reports.sort(key=lambda fn: os.path.getatime(reportfile + '/' + fn))
        file = os.path.join(reportfile, reports[-1])
        email.email(file)
