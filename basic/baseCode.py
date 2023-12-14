#!/bin/env python
#coding=utf-8
from enum import Enum

# 基础模块python代码练习
# https://www.runoob.com/python3/python3-data-structure.html
# 集合遍历处理
def listForSkill():
    a = [66.25, 333, 333, 1, 1234.5]
    for index,value in enumerate(a):
        print('获取的值是:' + str(value))

# 字典类型处理
def dictForSkill():
    knights = {'gallahad': 'the pure', 'robin': 'the brave'}
    for key,value in knights.items():
        print(value)
    table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
    for name,number in table.items():
        print('{0:10} ===> {1:10d}'.format(name, number))

# 枚举对象
class People(Enum):
    YELLOW_RACE = '黄种人'
    WHITE_PERSON = '白种人'
    BLACK_RACE = '黑种人'
    DEFULT = 0

# 迭代枚举
def forEnum():
    for item in People:
        print(item.name, ' : ', item.value)

# 错误对象
class MyError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# 捕获异常
def fileException():
    try:
        f = open("1.txt")
        s = f.readline()
        i = int(s.strip())
    except ValueError:
        print("catch valueError info....")
    except:
        print("catch exception...")
    finally:
        print("finnaly执行的代码")

if __name__ == '__main__':
    #dictForSkill()
    forEnum()