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
import core.mylog as log
import core.myrequest as request
import model.model as mm
import model.report as mr
import util.others as others

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
income_id = None
balance = None
withdraw_id = None
pro_withdraw_id = None


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
                log_message = "预期code:%s \n" % expect_code + "实际code:%s \n" % actual_code + "预期结果和实际结果不一致"
            else:
                logging.info("接口测试成功")
                test_status = "成功"
                pass_result = pass_result + 1
                log_message = "预期code:%s\n" % expect_code + "实际code:%s\n" % actual_code + "预期结果和实际结果相同"
            summary_report = self.excReport.sum_result(url, api_url, method, name, run_time, test_status, log_message)

        total_end = others.get_now()[0]
        total_run_time = str(others.get_mills(total_start, total_end)) + 'ms'
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

    def execute_case_proproject(self, filename):
        """
        :param filename: 用例文件名称
        :return: 测试结果的报告模板
        企业项目发布流程回归测试
        """
        global summary_report, single_start, single_end, content, message, result, code
        global project_id, quote_id, project_name, confirm_id, sub_projectId, contract_id, plan_id
        global qiniu_token, qiniu_hash, qiniu_key, qiniu_upkey, delivery_name, asset_id, income_id
        global balance, withdraw_id, pro_withdraw_id

        report_title = cs.PRO_REPORT_TITLE
        rc.get_config(filename)
        case_list = eval(rc.get_title_list())
        all_result = len(case_list)
        pass_result = 0
        fail_result = 0
        total_start = others.get_now()[0]
        project_name = "测试项目" + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        delivery_time = str(others.get_future(60))

        for i in range(0, all_result):
            title = case_list[i]
            number = str(rc.get_data(title, key=cs.NUMBER))
            name = str(rc.get_data(title, key=cs.NAME))
            data = eval(rc.get_data(title, key=cs.DATA))
            api_url = str(rc.get_data(title, key=cs.URL))
            method = str(rc.get_data(title, key=cs.METHOD))
            headers = eval(rc.get_data(title, key=cs.HEADERS))
            url = cs.BASEURL + api_url

            if number == '1':
                data['projectName'] = project_name
                data['deliveryTime'] = delivery_time
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)

                logging.info("解析出来的企业项目信息 %s" % content)

                if content is None:
                    raise ValueError('返回值为空。。。%s' % content)

                if content['code'] == '0':
                    project_id = content['result']['projectId']
                else:
                    pass
            if number == '2':
                url = url % project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '3':
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '4':
                url = url % project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    quote_id = content["result"]["quoteInfo"]["id"]
                else:
                    pass
            if number == '5':
                data['id'] = quote_id
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '6':
                data['id'] = quote_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '7':
                data['id'] = quote_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '8':
                project_id = project_id
                quote_id = quote_id
                url = url % (quote_id, project_id)
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '9':
                data['id'] = project_id
                data['projectName'] = project_name + "子项目"
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '10':
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    confirm_id = content['result']
                else:
                    pass
            if number == '11':
                project_id = project_id
                url = url % project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '12':
                url = url % confirm_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    sub_projectId = content['result']['projectId']
                else:
                    pass
            if number == '13':
                data['confirmId'] = confirm_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '14':
                data['projectId'] = sub_projectId
                data['planStartTime'] = str(others.get_now())[2]
                data['planEndTime'] = delivery_time
                data['vProjectId'] = cs.VPROJECT_ID
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '15':
                data['projectId'] = sub_projectId
                data['planStartTime'] = str(others.get_now())[2]
                data['planEndTime'] = delivery_time
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '16':
                data['projectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '17':
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '18':
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    contract_id = content['result']['contractId']
                else:
                    pass
            if number == '19':
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '20':
                url = url % contract_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '21':
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    plan_id = content['result']['planList'][0]['id']
                else:
                    pass
            if number == '22':
                data['projectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '23':
                data['projectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '24':
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
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
            if number == '26':
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    asset_id = content['result']['resourceList'][0]['id']
                else:
                    pass
            if number == '27':
                data['assetId'] = asset_id
                data['planId'] = plan_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '28':
                data['projectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '29':
                data['contractId'] = contract_id
                data['planId'] = plan_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '30':
                data['proProjectId'] = sub_projectId
                data['planId'] = plan_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '31':
                url = url % sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '32':
                url = url % sub_projectId
                data['proProjectId'] = sub_projectId
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '33':
                data['projectId'] = project_id
                data['productList'][0]['id'] = asset_id
                data['productList'][0]['assetId'] = asset_id
                data['productList'][0]['proProjectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '34':
                data['projectId'] = project_id
                data['reportList'][0]['id'] = asset_id
                data['reportList'][0]['assetId'] = asset_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '35':
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '108117':
                    content['message'] = 'success'
                    content['result'] = '异常操作流程：error code-108117项目没有设置账期和收款金额，不能开启账期'
                else:
                    pass
            if number == '36':
                data['id'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '37':
                data['projectId'] = project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '38':
                url = url % project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '39':
                data['vProjectId'] = cs.VPROJECT_ID
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '40':
                url = url % cs.VPROJECT_ID
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    income_id = content['result'][0]['id']
                else:
                    pass
            if number == '41':
                data['id'] = income_id
                data['vProjectId'] = cs.VPROJECT_ID
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '42':
                data['projectIds'][0] = sub_projectId
                data['vProjectId'] = cs.VPROJECT_ID
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '43':
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    balance = content['result']['balance']
                else:
                    pass
            if number == '44':
                if balance > 100:
                    content = request.get_message(method=method, url=url, data=data, headers=headers)
                    if content['code'] == '0':
                        withdraw_id = content['result']['withdrawId']
                    else:
                        pass
                else:
                    pass
            if number == '45':
                url = url % withdraw_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '46':
                data['proProjectIds'][0] = sub_projectId
                data['withdrawId'] = withdraw_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '47':
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                if content['code'] == '0':
                    rows = len(content['result']['list'])
                    for row in range(rows):
                        if content['result']['list'][row]['projectName'] == project_name + "子项目":
                            pro_withdraw_id = content['result']['list'][row]['projectWithdrawId']
                else:
                    pass
            if number == '48':
                url = url % pro_withdraw_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '49':
                url = url % pro_withdraw_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
            if number == '50':
                url = url % project_id
                content = request.get_message(method=method, url=url, data=json.dumps(data), headers=headers)
                # if content['result']['projectStatus'] == 8:
                #     logging.info("企业项目完结")
            try:
                if content != None:
                    if content['result'] != None:
                        code = content['code']
                        message = content['message']
                        result = content['result']
                    else:
                        code = content['code']
                        message = content['message']
                        result = None
                else:
                    message = None

                if message == 'success':
                    logging.info("企业项目发布流程回归测试通过:%s" % name)
                    test_status = "成功"
                    pass_result = pass_result + 1
                    log_message = "result:%s\n" % result
                else:
                    logging.info("企业项目发布流程回归测试失败:%s" % name)
                    test_status = "失败"
                    fail_result = fail_result + 1
                    log_message = "code:%s\n" % code + "message:%s\n" % message + "result:%s\n" % result

            except Exception as e:
                logging.error("无返回结果%s" % e)
                log_message = e
            if content is not None:
                run_time = str(content['run_time']) + 's'
            summary_report = self.excReport.sum_result(url, api_url, method, name, run_time, test_status, log_message)

        total_end = others.get_now()[0]
        total_run_time = str(others.get_mills(total_start, total_end)) + 's'
        skip_result = all_result - (pass_result + fail_result)
        report_model = mm.ReportModel(summary_report, report_title, all_result, pass_result, fail_result, skip_result,
                                      total_run_time)
        return report_model

    def build_report_proproject(self, filename):
        test_report = self.execute_case_proproject(filename)
        self.excReport.build_report(test_report.sum_report, test_report.name, test_report.pass_test,
                                    test_report.fail_test, test_report.skip_test, test_report.total_run_time)

    def send_email_proproject(self, reportfile):
        reports = os.listdir(reportfile)
        reports.sort(key=lambda fn: os.path.getatime(reportfile + '/' + fn))
        file = os.path.join(reportfile, reports[-1])
        email.email(file)
