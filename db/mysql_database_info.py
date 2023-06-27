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
end_sql_iceberg = "`ds`				string," + "\n" +  "`sink_time` string " + "\n" + " ) USING iceberg PARTITIONED  BY  (ds); "
end_sql_hive = """`etl_name`                                      string comment 'ETL名称',
`etl_time`                                      string comment 'ETL时间'
) 
row format delimited
fields terminated by ','
STORED AS TEXTFILE;
"""

# mysql ddl info
mysql_ddl_sql = 'show create table '
mysql_index_sql = 'show index from '

# sqoop 字符串配置
sqoop_delete_sql = 'sqoop eval --connect jdbc:mysql://127.0.0.1:3306/xxxx_warehouse --username root --password 123456 --query "delete from {0}"'
sqoop_insert_from_hive = "sqoop export --connect jdbc:mysql://127.0.0.1:3306/xxxx_warehouse --username root --password 123456 --table {0} --input-null-string '\\N' --input-null-non-string '\\N'  --input-fields-terminated-by ',' --table ods_{0} --hcatalog-database xxx -hcatalog-table ods_{0} -m 1"
sqoop_import_shell = """
sqoop import --connect jdbc:mysql://127.0.0.1:3306/xxxx --username root --password '123456' --table {0} --hive-import --hive-overwrite --hive-database xxx --hive-table ods_{0} --hive-partition-key ds --hive-partition-value xxxx_date --fields-terminated-by '\t' -m 1
"""

# table info
tableInfoList = [
    't_leid_form_head',
    't_leid_form_head_l',
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
    't_leid_classify_detail_a',
    't_leid_form_field',
    't_bdeq_ent_target_value'
]

# 传入文件名字 和 文件内容;将文件内容写入到文件中
def writeStrToFile(fileName,fileContent):
    with open(fileName,'w') as f:
        f.write(fileContent)

# 根据读取 mysql 的表字段信息,组建 iceberg 表
def createIcebergDdl(sqlType):
    all_md_sql = ''
    
    for index,value in enumerate(tableInfoList):
        query_sql = show_full_sql + value
        cursor.execute(query_sql)
        info=cursor.fetchall()
        one_sql = create_sql_iceberg + value + " ( " + "\n"
        
        all_md_sql += '## ' + value
        all_md_sql += '\n'
        all_md_sql += '```sql'
        all_md_sql += '\n'
        all_len = len(info) - 1
        for fIndex,fValue in enumerate(info):
            one_row_sql = parseOneRowSql(fValue)
            one_sql += one_row_sql
            one_sql += '\n'
        
        one_sql += (end_sql_iceberg if 'iceberg' == sqlType else end_sql_hive)
        
        all_md_sql += one_sql
        all_md_sql += '\n'
        all_md_sql += '```'
        all_md_sql += '\n'
        # print(one_sql)
    # all_md_sql  是拼接成 markdown 语法例子
    print(all_md_sql)

# 解析单行sql语句
def parseOneRowSql(fValue):
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
    return field_name + '				' + iceberg_field_type  + ','

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
             
        
def addColumeInfo():
    sql_prefix = "ALTER TABLE gyyt."
    sql_end = " ADD COLUMNS ( sink_time string comment 'write data time' );"
    for index,value in enumerate(tableInfoList):
        alter_sql = sql_prefix + value + sql_end
        print(alter_sql)

def sqoopFormatShell():
    all_sqoop_shell = ''
    for index,value in enumerate(tableInfoList):
        all_sqoop_shell += '## ' + value  + '\n'
        all_sqoop_shell += '```shell'
        all_sqoop_shell += '\n'
        new_sqoop_delete_sql = sqoop_delete_sql.format(value)
        new_sqoop_insert_from_hive = sqoop_insert_from_hive.format(value)
        all_sqoop_shell += new_sqoop_delete_sql + '\n'
        all_sqoop_shell += new_sqoop_insert_from_hive + '\n'
        all_sqoop_shell += '```'
        all_sqoop_shell += '\n'
    #print(all_sqoop_shell)
    new_sqoop_import_shell =  sqoop_import_shell.format('t_leid_form_head_l')
    print(new_sqoop_import_shell)
        
if __name__ == '__main__':
    #createIcebergDdl('hive')
    #readMySqlDdlInfo()
    #readIndexInfoFromTable()
    #addColumeInfo()
    sqoopFormatShell()