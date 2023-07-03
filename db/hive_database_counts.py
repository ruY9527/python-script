
from impala.dbapi import connect

conn = connect(host='bigdata01', port=10000, auth_mechanism='PLAIN', database='funing_db_ind')
cursor = conn.cursor()
hive_count_sql_base = "select count(*) from "

'''
需要按照的依赖:
安装 pure-sasl
pip install pure-sasl
安装 thrift_sasl
pip install thrift_sasl==0.2.1 --no-deps
安装thrift
pip install thrift_sasl==0.2.1 --no-deps
安装最终的:impyla
pip install impyla
pip install thriftpy
'''

# 获取hive某个库的全部count数据;注意每个 count 方法比较慢
def readHiveDatabaseCounts():
    cursor.execute('show tables')
    all_counts = 0
    tables = cursor.fetchall()
    for index,value in enumerate(tables):
        table_name = value[0]
        hive_count_sql = hive_count_sql_base + table_name
        cursor.execute(hive_count_sql)
        one_table_count = cursor.fetchall()
        one_count =  one_table_count[0]
        print(one_count[0])
        all_counts += one_count[0]

    print(all_counts)


if __name__ == '__main__':
    main()
    