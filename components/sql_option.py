import mysql.connector

import pandas as pd
import streamlit as st


# 连接数据库
def database_connection():
    conn = mysql.connector.connect(
        host='vango-cms-prod-outer.mysql.rds.aliyuncs.com',
        user='dlzdaily',
        passwd='x&sKFQz#@Tq%7GE',
        port=4210,
        db="dlz-daily-records",
        charset='utf8mb4'
    )
    cursor = conn.cursor(prepared=True)
    return conn, cursor


# 获取定制信息规则
def get_rules():
    conn, cursor = database_connection()
    cursor.execute("select type, english, chinese from rules order by type asc, chinese asc, english asc")
    result = cursor.fetchall()
    data = pd.DataFrame(result, columns=["类型", "英文表述", "中文表述"])
    cursor.close()
    conn.close()
    return data
