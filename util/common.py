#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 主要公用方法

import core.myconfig as rc
import os
import core.myrequest as request
import json
import constants as cs
import core.mylog as log
import core.myemail as email
import model.report as mr
import model.model as mm
import random, string
import util.others as others
import datetime

logging = log.track_log()
summary_report = []
single_start = datetime.datetime.now()
single_end = datetime.datetime.now()
content = None
code = None
message = None
result = None
project_id = None
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


""" 接口404时，返回未处理？？？"""


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
        global summary_report, single_start, single_end
        report_title = cs.REPORT_TITLE
        rc.get_config(filename)
        case_list = eval(rc.get_title_list())
        all_result = len(case_list)
        pass_result = 0
        fail_result = 0
        total_start = others.get_now()[0]

        for i in range(0, all_result):
            title = case_list[i]
            name = rc.get_data(title, key=cs.NAME)
            method = rc.get_data(title, key=cs.METHOD)
            code = rc.get_data(title, key=cs.CODE)
            api_url = rc.get_data(title, key=cs.URL)
            url = cs.BASEURL + api_url
            headers = eval(rc.get_data(title, key=cs.HEADERS))
            _data = eval(rc.get_data(title, key='data'))
            data = json.dumps(_data, indent=4, sort_keys=False, ensure_ascii=False)
            single_start = others.get_now()[0]
            actual_code = request.api(method, url, data, headers)
            single_end = others.get_now()[0]
            expect_code = code
            run_time = str(others.get_mills(single_start, single_end)) + 'ms'

            if actual_code != expect_code:
                logging.info("接口测试失败")
                test_status = "失败"
                fail_result = fail_result + 1
                log_message = "预期code:%s \n" %expect_code + "实际code:%s \n" % actual_code + "预期结果和实际结果不一致"
            else:
                logging.info("接口测试成功")
                test_status = "成功"
                pass_result = pass_result + 1
                log_message = "预期code:%s\n" %expect_code + "实际code:%s\n" % actual_code + "预期结果和实际结果相同"
            summary_report = self.excReport.sum_result(url, api_url, method, name, run_time, test_status, log_message)

        total_end = others.get_now()[0]
        total_run_time = str(others.get_mills(total_start, total_end)) + 'ms'
        skip_result = all_result-(pass_result + fail_result)
        report_model = mm.ReportModel(summary_report, report_title, all_result, pass_result, fail_result, skip_result,
                                      total_run_time)
        return report_model

    def build_report(self, filename):
        test_report = self.execute_case(filename)
        self.excReport.build_report(test_report.sum_report, test_report.name, test_report.pass_test,
                                  test_report.fail_test, test_report.skip_test, test_report.total_run_time)

    def send_email(self, reportfile):
        reports = os.listdir(reportfile)
        reports.sort(key=lambda fn: os.path.getatime(reportfile+'/'+fn))
        file = os.path.join(reportfile, reports[-1])
        email.email(file)


class ProProjectRegression:
    excReport = mr.Report()

    def __init__(self):
        pass

    def execute_case_proprojectreg(self, filename):
        """
        :param filename: 用例文件名称
        :return: 测试结果的报告模板
        企业项目发布流程回归测试
        Note： python没有Null，用None代表Null
        """
        global summary_report, single_start, single_end, content, message, result, code
        global project_id, quote_id, project_name, confirm_id, sub_projectId, contract_id, plan_id
        global qiniu_token, qiniu_hash, qiniu_key, qiniu_upkey, delivery_name, asset_id
        report_title = cs.REPORT_TITLE
        rc.get_config(filename)
        case_list = eval(rc.get_title_list())
        all_result = len(case_list)
        pass_result = 0
        fail_result = 0
        total_start = others.get_now()[0]
        project_name = "测试项目" + ''.join(random.sample(string.ascii_letters + string.digits, 4))


        # try:
        for i in range(0, all_result):
            title = case_list[i]
            number = str(rc.get_data(title, key=cs.NUMBER))
            name = str(rc.get_data(title, key=cs.NAME))
            data = eval(rc.get_data(title, key=cs.DATA))
            # data = json.dumps(_data, indent=4, sort_keys=False, ensure_ascii=False)
            api_url = str(rc.get_data(title, key=cs.URL))
            method = str(rc.get_data(title, key=cs.METHOD))
            headers = eval(rc.get_data(title, key=cs.HEADERS))
            # _headers = json.dumps(headers, indent=2, sort_keys=False, ensure_ascii=False)
            url = cs.BASEURL + api_url
            run_time = str(others.get_mills(single_start, single_end)) + 'ms'
            delivery_time = str(others.get_future(60))
            # project_name = "测试项目" + ''.join(random.sample(string.ascii_letters + string.digits, 4))

            if number == '1':
                data['projectName'] = project_name
                data['deliveryTime'] = delivery_time
                single_start = others.get_now()[0]
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    project_id = content['result']['projectId']
                else:
                    pass
            if number == '2':
                single_start = others.get_now()[0]
                url = url % project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '3':
                single_start = others.get_now()[0]
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '4':
                single_start = others.get_now()[0]
                url = url %project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    quote_id = content["result"]["quoteInfo"]["id"]
                else:
                    pass
            if number == '5':
                single_start = others.get_now()[0]
                data['id'] = quote_id
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '6':
                single_start = others.get_now()[0]
                data['id'] = quote_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '7':
                single_start = others.get_now()[0]
                data['id'] = quote_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '8':
                single_start = others.get_now()[0]
                project_id = project_id
                quote_id = quote_id
                url = url % (quote_id,project_id)
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            # 确认函请求data里的时间戳还没处理？？
            if number == '9':
                single_start = others.get_now()[0]
                data['id'] = project_id
                data['projectName'] = project_name + "子项目"
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '10':
                single_start = others.get_now()[0]
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    confirm_id = content['result']
                else:
                    pass
            if number == '11':
                single_start = others.get_now()[0]
                project_id = project_id
                url = url % project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '12':
                single_start = others.get_now()[0]
                url = url % confirm_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    sub_projectId = content['result']['projectId']
                else:
                    pass
            if number == '13':
                single_start = others.get_now()[0]
                data['confirmId'] = confirm_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '14':
                single_start = others.get_now()[0]
                data['projectId'] = sub_projectId
                data['planStartTime'] = str(others.get_now())[2]
                data['planEndTime'] = delivery_time
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '15':
                single_start = others.get_now()[0]
                data['projectId'] = sub_projectId
                data['planStartTime'] = str(others.get_now())[2]
                data['planEndTime'] = delivery_time
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '16':
                single_start = others.get_now()[0]
                data['projectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '17':
                single_start = others.get_now()[0]
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '18':
                single_start = others.get_now()[0]
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    contract_id = content['result']['contractId']
                else:
                    pass
            if number == '19':
                single_start = others.get_now()[0]
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '20':
                single_start = others.get_now()[0]
                url = url % contract_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '21':
                single_start = others.get_now()[0]
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    plan_id = content['result']['planList'][0]['id']
                else:
                    pass
            # 此接口需要调用两次才成功，和开发确认为什么？
            if number == '22':
                single_start = others.get_now()[0]
                data['projectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '23':
                single_start = others.get_now()[0]
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    qiniu_token = content['result']['token']
                    qiniu_key = content['result']['key']
                else:
                    pass
            # if number == '24':
            #     single_start = others.get_now()[0]
            #     url = 'https://upload.qiniup.com/'
            #     content = request.get_mfd(method=method, url=url, data=data, headers=headers)
            #     single_end = others.get_now()[0]
            #     if content.get('code') == 0:
            #         qiniu_hash = content.get('hash')
            #         qiniu_upkey = content.get('key')
            #     else:
            #         pass
            if number == '25':
                single_start = others.get_now()[0]
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
                if content['code'] == '0':
                    asset_id = content['result']['resourceList'][0]['id']
                else:
                    pass
            if number == '26':
                single_start = others.get_now()[0]
                data['assetId'] = asset_id
                data['planId'] = plan_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '27':
                single_start = others.get_now()[0]
                data['projectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '28':
                single_start = others.get_now()[0]
                data['contractId'] = contract_id
                data['planId'] = plan_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '29':
                single_start = others.get_now()[0]
                data['proProjectId'] = sub_projectId
                data['planId'] = plan_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '30':
                single_start = others.get_now()[0]
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]
            if number == '31':
                single_start = others.get_now()[0]
                url = url % sub_projectId
                data['proProjectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                single_end = others.get_now()[0]

            try:
                if content != None:
                    if content['result'] != None:
                        code = content['code']
                        message = content['message']
                        result = content['result']
                    else:
                        code = content['code']
                        message = content['message']
                else:
                    message = None

                if message == 'success':
                    logging.info("企业项目发布流程回归测试通过:%s" % name)
                    test_status = "成功"
                    pass_result = pass_result + 1
                    log_message = "message:%s\n" % message + "result:%s\n" % result
                else:
                    logging.info("企业项目发布流程回归测试失败:%s" %name)
                    test_status = "失败"
                    fail_result = fail_result + 1
                    log_message = "code:%s\n" % code + "message:%s\n" %message + "result:%s\n" % result

            except Exception as e:
                logging.error("无返回结果%s" % e)
                log_message = e
            summary_report = self.excReport.sum_result(url, api_url, method, name, run_time, test_status, log_message)

        total_end = others.get_now()[0]
        total_run_time = str(others.get_mills(total_start, total_end)) + 'ms'
        skip_result = all_result-(pass_result + fail_result)
        report_model = mm.ReportModel(summary_report, report_title, all_result, pass_result, fail_result, skip_result,
                                      total_run_time)
        return report_model
        # except Exception as e:
        #     logging.error("执行失败，%s" %e)

    def build_report_proprojectreg(self, filename):
        test_report = self.execute_case_proprojectreg(filename)
        self.excReport.build_report(test_report.sum_report, test_report.name, test_report.pass_test,
                                test_report.fail_test, test_report.skip_test, test_report.total_run_time)

    def send_email_proprojectreg(self, reportfile):
        reports = os.listdir(reportfile)
        reports.sort(key=lambda fn: os.path.getatime(reportfile+'/'+fn))
        file = os.path.join(reportfile, reports[-1])
        email.email(file)

# a = ProProjectRegression()
# casefile = os.getcwd() +'/case/proProjectRegression_origin.ini'
# a.build_report_proprojectreg(casefile)

