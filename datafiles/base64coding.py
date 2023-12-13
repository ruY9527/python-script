#coding=utf-8

import base64

sql = 'select * from tongchuang.dim_enterprise ;'

base64_str = base64.b64encode(sql.encode('utf-8'))

print(type(str(base64_str)))
print(base64_str.decode('utf-8'))