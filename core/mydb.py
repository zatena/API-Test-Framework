#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：数据库

import pymysql.cursors
import core.mylog as log

logging =log.track_log()
con = None

def connect_db(host, user, password, db, charset='utf8'):
    """连接MySQL"""
    global con
    if con == None:
        con = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset,
                             cursorclass=pymysql.cursors.DictCursor)
    return con

def execute_sql(sql):
    """执行sql语句"""
    global con
    try:
        cursor = con.cursor()
        result = cursor.execute(sql)
        con.commit()
        return result
    except Exception as e:
        logging.error("执行sql失败:%s" %e)
        con.rollback()

def close_db():
    """关闭MySQL"""
    global con
    con.close()
