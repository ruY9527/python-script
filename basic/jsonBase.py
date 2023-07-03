#!/usr/bin/python3

import json
import time

data = {
    'no' : 1,
    'name' : 'BaoYang',
    'url' : 'https://www.baoyang.xyz'
}

def dictToStr():
    json_str = json.dumps(data)
    print("python 的原始对象: " + repr(data))
    print("json 字符串: " + json_str)

    data_json = json.loads(json_str)
    print(data_json['name'])

def dictWirteRead():
    with open('data1.json', 'w') as f:
        json.dump(data,f)
    time.sleep(3)
    with open('data1.json', 'r') as f:
        data1 = json.load(f)
        print(data1)

if __name__ == '__main__':
    dictWirteRead()
    
    