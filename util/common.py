#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 主要公用方法

import datetime
import json
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

from core.myhtmlparser import MyHTMLParser
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
project_id = 2258
quote_id = None
project_name = None
confirm_id = None
sub_projectId = None
contract_id = None
plan_id = None
qiniu_token = None
qiniu_hash = None
qiniu_key = None
qiniu_upkey = None
delivery_name = others.get_filename(cs.DELIVERY_PATH)
asset_id = None
income_id = None
balance = None
withdraw_id = None
pro_withdraw_id = None
collect_data = {}
pass_result = 0
fail_result = 0
skip_result = 0


class ApiTest:
    excReport = mr.Report()

    """业务接口测试"""

    def __init__(self):
        pass

    def execute_case(self, filename):

        """
        :param filename: 用例文件名称
        :return: 测试结果的报告模板
        """
        global summary_report, single_start, single_end, pass_result, fail_result, skip_result
        report_title = cs.REPORT_TITLE
        case_names = rc.get_casename(filename)[0]
        case_lists = rc.get_casename(filename)[1]
        all_result = len(case_names)
        total_start = others.get_now()[0]

        try:
            for i in range(0, all_result):
                case_list = case_lists['steps'][i]
                name = case_names[i]
                method = case_list['caseMethod']
                expect_code = case_list['assertions']['body']['code']
                headers = case_list['request']['headers']
                api_url = case_list['caseUrl']
                url = cs.BASEURL + api_url
                _data = case_list['request']['body']

                if len(collect_data) > 0:
                    str_data = str(case_list)
                    match_object = re.findall('.*?([\u4E00-\u9FA5]+\.[\\w]+)', str_data)
                    if len(match_object) == 0:
                        pass
                    else:

                        for i in match_object:
                            collect_response = collect_data[i.split('.')[0]]
                            actual_value = i.split('.')[1]
                            replace_value = getRelyValues.get_dict(collect_response, actual_value)
                            str_data = str_data.replace(i, str(replace_value))
                            data_json = eval(str_data)
                            headers = data_json['request']['headers']
                            api_url = data_json['caseUrl']
                            url = cs.BASEURL + api_url
                            _data = data_json['request']['body']
                else:
                    pass

                data = json.dumps(_data, indent=4, sort_keys=False, ensure_ascii=False)
                data = data.encode('utf-8')
                single_start = others.get_now()[0]
                actual_response = request.api(method, url, data, headers)
                single_end = others.get_now()[0]
                actual_code = actual_response['code']
                collect_data[name] = actual_response
                run_time = str(others.get_mills(single_start, single_end)) + 's'

                if actual_code != expect_code:
                    logging.info("接口测试失败")
                    test_status = "失败"
                    fail_result = fail_result + 1
                    message_log = "预期code:%s \n" % expect_code + "实际code:%s \n" % actual_code + "预期结果和实际结果不一致"
                else:
                    logging.info("接口测试成功")
                    test_status = "成功"
                    pass_result = pass_result + 1
                    message_log = "预期code:%s\n" % expect_code + "实际code:%s\n" % actual_code + "预期结果和实际结果相同"
                summary_report = self.excReport.sum_result(url, api_url, method, name, run_time, test_status, message_log)
        except Exception as e:
            logging.error(e)

        total_end = others.get_now()[0]
        total_run_time = str(others.get_mills(total_start, total_end)) + 's'
        skip_result = all_result - (pass_result + fail_result)
        report_model = mm.ReportModel(summary_report, report_title, all_result, pass_result, fail_result, skip_result,
                                      total_run_time)
        return report_model



    def build_report(self, filename):
        test_report = self.execute_case(filename)
        self.excReport.build_report(test_report.sum_report, test_report.name, test_report.pass_test,
                                    test_report.fail_test, test_report.skip_test, test_report.total_run_time)

    def send_email(self, reportfile):
        reports = os.listdir(reportfile)
        reports.sort(key=lambda fn: os.path.getatime(reportfile + '/' + fn))
        file = os.path.join(reportfile, reports[-1])
        email.email(file)


class ProProjectRegression:
    excReport = mr.Report()

    def __init__(self):
        pass

    def execute_case_regression(self, filename):
        """
        :param filename: 用例文件名称
        :return: 测试结果的报告模板

        """
        global summary_report, message, result, code
        global project_id, quote_id, project_name, confirm_id, sub_projectId, contract_id, plan_id
        global qiniu_token, qiniu_hash, qiniu_key, qiniu_upkey, delivery_name, asset_id, income_id
        global balance, withdraw_id, pro_withdraw_id, pass_result, fail_result, skip_result

        report_title = cs.TEST_REPORT_TITLE
        case_names = rc.get_casename(filename)[0]
        case_lists = rc.get_casename(filename)[1]
        all_result = len(case_names)
        total_start = others.get_now()[0]
        project_name = "测试项目" + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        delivery_time = str(others.get_future(60))
        caseScenario = case_lists['scenarioName']

        try:
            for i in range(0, all_result):
                case_list = case_lists['steps'][i]
                name = case_names[i]
                method = case_list['caseMethod']
                expect_body = case_list['assertions']['body']
                expect_code = expect_body['code']
                expect_assert = None
                if len(expect_body) == 2:
                    expect_assert = expect_body['assert']
                assert_len = 0
                str_data = str(case_list)
                if len(collect_data) > 0:
                    match_object = re.findall('.*?([\u4E00-\u9FA5]+\.[\\w]+)', str_data)
                    expect_assert_name = str(expect_assert).split(":")[0]
                    if expect_assert_name in match_object:
                       match_object.remove(expect_assert_name)
                    if len(match_object) == 0:
                        pass
                    else:
                        for i in match_object:
                            collect_response = collect_data[i.split('.')[0]]
                            res_code = getRelyValues.get_dict(collect_response, 'code')
                            if int(res_code) > 0:
                                continue
                            actual_value = i.split('.')[1]
                            replace_value = getRelyValues.get_dict(collect_response, actual_value)
                            str_data = str_data.replace(i, str(replace_value))
                            data_json = eval(str_data)
                            headers = data_json['request']['headers']
                            api_url = data_json['caseUrl']
                            url = cs.BASEURL + api_url
                            _data = data_json['request']['body']
                else:
                    pass
                str_data = str_data.replace('发布企业项目.projectName', project_name)
                str_data = str_data.replace('发布企业项目.deliveryTime', delivery_time)
                data_json = eval(str_data)
                headers = data_json['request']['headers']
                api_url = data_json['caseUrl']
                url = cs.BASEURL + api_url
                _data = data_json['request']['body']
                data = json.dumps(_data, indent=4, sort_keys=False, ensure_ascii=False)
                data = data.encode('utf-8')
                actual_response = request.get_message(method, url, data, headers)
                collect_data[name] = actual_response

                if expect_assert is not None:
                    assert_object = re.findall('.*?([\u4E00-\u9FA5]+\.[\\w]+)', expect_assert)
                    for k in assert_object:
                        res_str = k.split('.')[1]
                        assert_replace_value = getRelyValues.get_dict(actual_response, res_str)
                        k = expect_assert.replace(k, str(assert_replace_value))
                        assert_list = k.split(":")
                        assert_len = len(set(assert_list))

                try:
                    if actual_response is not None:
                        if actual_response['result'] != None:
                            actual_code = actual_response['code']
                            actual_message = actual_response['message']
                            actual_result = actual_response['result']
                            actual_status_code = None
                        else:
                            actual_code = actual_response['code']
                            actual_message = actual_response['message']
                            actual_result = None
                            if actual_code == -1:
                                actual_status_code = actual_response['status_code']
                            else:
                                actual_status_code = None

                    if actual_status_code is not None:
                        logging.info("回归测试失败:%s" % name)
                        test_status = "失败"
                        fail_result = fail_result + 1
                        log_message = "code:%s\n" % actual_status_code

                    elif actual_code == expect_code and expect_assert is None:
                        logging.info("回归测试通过:%s" % name)
                        test_status = "成功"
                        pass_result = pass_result + 1
                        log_message = "code:%s\n" % actual_code + "message:%s\n" % actual_message + "result:%s\n" % actual_result

                    elif assert_len == 1:
                        logging.info("回归测试通过:%s" % name)
                        test_status = "成功"
                        pass_result = pass_result + 1
                        log_message = "code:%s\n" % actual_code + "message:%s\n" % actual_message + "result:%s\n" % actual_result

                    else:
                        logging.info("回归测试失败:%s" % name)
                        test_status = "失败"
                        fail_result = fail_result + 1
                        if assert_len > 1:
                            actual_result = "实际结果:%s\n" % k[0] + "预期结果:%s\n" % k[2]
                        log_message = "code:%s\n" % actual_code + "message:%s\n" % actual_message + "result:%s\n" % actual_result

                except Exception as e:
                    logging.error("无返回结果%s" % e)
                    traceback.print_exc()

                run_time = str(actual_response['run_time']) + 'ms'
                summary_report = self.excReport.sum_result(caseScenario, url, method, name, run_time, test_status, log_message)
        except Exception as e:
            logging.error(e)
            traceback.print_exc()

        total_end = others.get_now()[0]
        total_run_time = str(others.get_mills(total_start, total_end)) + 's'

        report_model = mm.ReportModel(summary_report, report_title, all_result, pass_result, fail_result, skip_result,
                                      total_run_time)

        return report_model

    def build_report_regression(self, filename):
        test_report = self.execute_case_regression(filename)
        self.excReport.build_report(test_report.sum_report, test_report.name, test_report.pass_test,
                                    test_report.fail_test, test_report.skip_test, test_report.total_run_time,email)

    def send_email_regression(self, reportfile):
        reports = os.listdir(reportfile)
        reports.sort(key=lambda fn: os.path.getatime(reportfile + '/' + fn))
        file = os.path.join(reportfile, reports[-1])
        email.email(file)
