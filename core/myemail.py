#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：邮件服务

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import constants as cs
import core.mylog as log

logging = log.track_log()


def email(reportfile):

    # mail_file = open(reportfile,'rb').read()
    att = MIMEText(reportfile, 'html', 'utf-8')
    att['ContentType'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment:filename="测试报告'

    message = MIMEMultipart('related')
    message['From'] = cs.MAIL_SENDER
    message['To'] = ','.join(cs.MAIL_RECEIVER)
    message['Subject'] = Header('接口自动化测试报告', 'utf-8')
    message.attach(att)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(cs.MAIL_HOST, 25)
        smtp.login(cs.MAIL_USER, cs.MAIL_PASS)
        smtp.sendmail(cs.MAIL_SENDER, message['To'].split(','), message.as_string())
        logging.info("**********发送邮件成功**********")
    except smtplib.SMTPException as e:
        logging.error("**********发送邮件失败:%s**********", e)
    finally:
        smtp.quit()

