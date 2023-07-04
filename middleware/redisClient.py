import redis
import json

# redis 连接

pool = redis.ConnectionPool(host='172.21.129.231',port=6379, password='kingdee$2020')
conn = redis.Redis(connection_pool=pool)


# 基本操作redis
def baseRedis():
    conn.set('redis1','redis1111')
    print(conn.get('redis1'))

def getInfoByKey():
    keyObj = conn.get('conn-dev-runlin:dataSync205022xxxx')
    print(type(keyObj))
    objStr = str(keyObj,'utf-8')
    objJson = json.loads(objStr)
    print(objJson)
    print(type(objJson))
    
        
if __name__ == '__main__':
    getInfoByKey()
    
