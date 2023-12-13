#coding=utf-8

import pymysql

db = pymysql.connect(host='bd214',user='root',passwd='YdMysqlxx9',db='funing_warehouse',port=3306,charset='utf8')
cursor = db.cursor()
mysql_count_sql = "select count(*) from " 
mysql_db_sql = '''
SELECT sum(table_rows) FROM information_schema.tables  
 WHERE TABLE_SCHEMA = '%s' 
 and table_name not in ('db','func') 
 ORDER BY table_rows DESC;
'''


def readAllCountByDb():
    count_sql = mysql_db_sql%'funing_warehouse'
    print(count_sql)
    cursor.execute(count_sql)
    all_count_one = cursor.fetchone()
    print(all_count_one[0])

def readMysqlDatabaseCount():
    cursor.execute("show tables");
    info = cursor.fetchall()
    allCount = 0
    for index,value in enumerate(info):
        count_sql = mysql_count_sql + value[0]
        cursor.execute(count_sql)
        ont_table_count = cursor.fetchall()
        allCount += ont_table_count[0][0]
    print(allCount)


if __name__ == '__main__':
    readAllCountByDb()
    