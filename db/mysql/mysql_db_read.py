import pymysql
import openpyxl

# 配置数据库连接信息
db_config = {
    'host': 'localhost',  # 你的MySQL地址
    'port': 3306,  # 端口
    'user': 'root',  # 用户名
    'password': 'baoyang',  # 密码
    'database': 'ruoyi-vue',  # 数据库名
    'charset': 'utf8mb4'
}

# 创建数据库连接
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# 查询所有表名
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# 创建一个新的Excel工作簿
workbook = openpyxl.Workbook()
# 删除默认创建的第一个空Sheet
workbook.remove(workbook.active)

for table in tables:
    table_name = table[0]

    # 创建新的sheet页
    sheet = workbook.create_sheet(title=table_name[:31])  # Sheet名称不能超过31字符

    # 写入表头
    headers = ["字段名称", "数据类型", "注释", "允许空"]
    sheet.append(headers)

    # 查询每个表的字段信息
    cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")
    columns = cursor.fetchall()

    for col in columns:
        field = col[0]  # 字段名称
        col_type = col[1]  # 数据类型
        is_nullable = col[3]  # 是否允许空 YES/NO
        comment = col[8]  # 注释

        row = [field, col_type, comment, is_nullable]
        sheet.append(row)

# 保存Excel文件
workbook.save('数据库表结构导出.xlsx')

# 关闭数据库连接
cursor.close()
connection.close()

print("导出成功，文件名：数据库表结构导出.xlsx")