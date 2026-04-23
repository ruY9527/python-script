#!/bin/env python
#coding=utf-8
import pymysql

db = pymysql.connect(host='172.21.129.214',user='root',passwd='YdMysqlxx9',db='db-user',port=3306,charset='utf8')
cursor = db.cursor()


# 读取区域code相关数据
def readAreaCode():
    # area_level3_sql = "SELECT name,short_name,merger_name FROM sys_area_code WHERE LEVEL=3 AND NAME LIKE '%自治%'"
    # area_level2_sql = "SELECT  name,short_name,merger_name FROM sys_area_code WHERE LEVEL=2 AND NAME LIKE '%自治%'"
    area_level1_sql = "SELECT  name,short_name,merger_name FROM sys_area_code WHERE LEVEL=1 AND NAME LIKE '%自治%'"
    cursor.execute(area_level1_sql)
    results = cursor.fetchall()
    all_remove_area = []
    for row in results:
        name = row[0]
        short_name = row[1]
        merger_name = row[2]
        self_name = name.replace(short_name, '')
        print(name + " ---- " + short_name + " ------ " +self_name)
        if self_name != '' and self_name not in all_remove_area:
            all_remove_area.append(self_name)
    all_remove_area.sort(key=lambda i: len(i), reverse=True)
    all_area_str = ''
    for index,value in enumerate(all_remove_area):
        if index != 0:
            all_area_str += ','
        all_area_str += value
    print(all_area_str)

if __name__ == '__main__':
    readAreaCode()