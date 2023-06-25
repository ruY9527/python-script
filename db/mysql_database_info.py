#!/bin/env python
#coding=utf-8

import pymysql

db = pymysql.connect(host='172.21.129.214',user='root',passwd='YdMysqlxx9',db='next_lec',port=3306,charset='utf8')
cursor = db.cursor()

# 查看表具体列的信息
# SHOW FULL FIELDS FROM enterprise_info;
# iceberg info
show_full_sql = "SHOW FULL FIELDS FROM "
create_sql_iceberg = "CREATE TABLE gyyt." 
end_sql_iceberg = " ) USING iceberg PARTITIONED  BY  (ds); "

# mysql ddl info
mysql_ddl_sql = 'show create table '
mysql_index_sql = 'show index from '

# table info
tableInfoList = [
    't_leid_form_head',
    't_leid_form_fill_record',
    't_iebd_org_id',
    't_lecpl_p_datastore',
    't_lec_area_code',
    't_bdeq_enterprise_target',
    't_bdeq_enterprise_target_l',
    't_iebd_enterprise',
    't_iebd_enterprise_l',
    't_relation_ent_ind',
    't_iebd_enterprisegroup',
    't_ent_type',
    't_iebd_enterprisetype',
    't_iebd_enterprisetype_l',
    't_leid_classify_scheme',
    't_leid_classify_result',
    't_leid_classify_detail_a'
]

# 根据读取 mysql 的表字段信息,组建 iceberg 表
def createIcebergDdl():
    for index,value in enumerate(tableInfoList):
        query_sql = show_full_sql + value
        cursor.execute(query_sql)
        info=cursor.fetchall()
        one_sql = create_sql_iceberg + value + " ( " + "\n"
        all_len = len(info) - 1
        for fIndex,fValue in enumerate(info):
            field_name = '`' + fValue[0] + '`'
            field_type = fValue[1]
            iceberg_field_type = ' string '
            if 'bigint' in field_type:
                iceberg_field_type = ' bigint '
            elif 'decimal' in field_type:
                iceberg_field_type = ' decimal(25,10) '
            elif 'int' in field_type:
                iceberg_field_type = ' bigint '
            elif 'datetime' in field_type:
                iceberg_field_type = ' string '
            #over_flag = ',' if all_len != fIndex else ''
            one_sql = one_sql + field_name + '				' + iceberg_field_type  + ','
            one_sql += '\n'
        one_sql += '`ds`				string' + "\n"
        one_sql += end_sql_iceberg
        print(one_sql)


# 读取 mysql 的 ddl 信息
def readMySqlDdlInfo():
    for index,value in enumerate(tableInfoList):
        query_mysql_ddl_sql = mysql_ddl_sql + value
        cursor.execute(query_mysql_ddl_sql)
        info=cursor.fetchall()
        ddl_sql = info[0][1]
        print(ddl_sql+";")
        print('\n')
     
     
def readIndexInfoFromTable():
    for index,value in enumerate(tableInfoList):
        query_index_sql = mysql_index_sql + value
        cursor.execute(query_index_sql)
        info=cursor.fetchall()
        print("\n")
        print("------------------开始表:" + value + "--------------------")
        for i in info:
            print(i[0])
            print(i[2])
            print(i[4])
             
        
if __name__ == '__main__':
    #createIcebergDdl()
    #readMySqlDdlInfo()
    readIndexInfoFromTable()