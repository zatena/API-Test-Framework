#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 生成报告方法封装


import os
import json
import shutil
import time

from model.htmlparser import MyHTMLParser

result = {
    "testPass": 1,
    "testResult": [
        {
            "serviceName": "com.test.testcase.TestDemo1",
            "serviceUrl": "http://test",
            "methodName": "post",
            "description": "测试DEMO",
            "spendTime": "11ms",
            "status": "成功",
            "log": [
                "this is demo!"
            ]
        },
        {
            "serviceName": "com.test.testcase.TestDemo1",
            "serviceUrl": "http://test",
            "methodName": "post",
            "description": "测试DEMO",
            "spendTime": "11ms",
            "status": "失败",
            "log": [
                "this is demo!"
            ]
        }
    ],
    "testName": "20171109132744898",
    "testAll": 1,
    "testFail": 0,
    "beginTime": "2017-11-09 13:27:44.917",
    "totalTime": "11ms",
    "testSkip": 0
}


class Report:

    testResultList = []

    def sum_result(self,scenario, serviceName, methodName, description, spendTime, status, requestlog, resulttlog):
        request_log = []
        result_log = []
        testResultDict = {}
        request_log.append(requestlog)
        result_log.append(resulttlog)

        # 汇总测试结果
        testResultDict["requestLog"] = request_log
        testResultDict["resultLog"] = result_log
        testResultDict["scenario"] = scenario
        testResultDict["serviceName"] = serviceName
        # testResultDict["serviceUrl"] = serviceUrl
        testResultDict["methodName"] = methodName
        testResultDict["description"] = description
        testResultDict["spendTime"] = spendTime
        testResultDict["status"] = status
        self.testResultList.append(testResultDict)
        return self.testResultList

    def build_report(self, testResult, testName, testPass, testFail, testSkip, totalTime, email):

        reportResult = {}
        reportResult["testPass"] = testPass
        reportResult["testResult"] = testResult
        reportResult["testName"] = testName
        reportResult["testAll"] = len(testResult)
        reportResult["testFail"] = testFail
        reportResult["beginTime"] = time.strftime("%Y-%m-%d %H:%M:%S")
        reportResult["totalTime"] = totalTime
        reportResult["testSkip"] = len(testResult)-testPass-testFail
        reportResult["testCoverage"] = str(round((float(testPass) / float(len(testResult)+testSkip)*100),2)) + '%'

        # 写入测试报告
        self.write_report(reportResult, testName)

        htmlparser = MyHTMLParser()
        htmltrs = htmlparser.reporthtmlparser(testResult,'')

        report = htmlparser.report_html.replace("${case_list}",htmltrs) \
            .replace("${filterAll}",str(len(testResult))) \
            .replace("${filterOk}",str(testPass)) \
            .replace("${filterFail}",str(testFail)) \
            .replace("${filterSkip}",str(len(testResult)-testPass-testFail)) \
            .replace("${filterCoverage}",str(round((float(testPass) / float(len(testResult)+testSkip)*100),2)) + '%')
        email.email(report)


    def write_report(self, reportResult, testName):
        reportHtmlFileName = testName + ".html"
        reportDirPath = os.path.dirname(os.path.realpath("report")) + "/report/"
        template = open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + "/model/template", "r", encoding='UTF-8')
        template = open(os.getcwd() + "/model/template", "r", encoding='UTF-8')
        reportHtml = open(reportHtmlFileName, "w", encoding='UTF-8')
        for s in template:
            reportHtml.write(s.replace("${resultData}", json.dumps(reportResult)))

        reportHtml.close()
        template.close()

        # 剪切文件到指定文件夹中 report
        if os.path.exists(reportDirPath):
            self.move_report(reportHtmlFileName,reportDirPath)

        else:
            os.makedirs(reportDirPath)
            self.move_report(reportHtmlFileName,reportDirPath)

    def move_report(self, fileName, dirPath):
        oldFilePath = os.path.realpath(fileName)
        newFilePath = dirPath + fileName
        shutil.move(oldFilePath, newFilePath)


