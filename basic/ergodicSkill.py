#!/bin/env python
#coding=utf-8

# https://www.runoob.com/python3/python3-data-structure.html
def listForSkill():
    a = [66.25, 333, 333, 1, 1234.5]
    for index,value in enumerate(a):
        print('获取的值是:' + str(value))

def dictForSkill():
    knights = {'gallahad': 'the pure', 'robin': 'the brave'}
    for key,value in knights.items():
        print(value)

    table = {'Google': 1, 'Runoob': 2, 'Taobao': 3}
    for name,number in table.items():
        print('{0:10} ===> {1:10d}'.format(name, number))

if __name__ == '__main__':
    dictForSkill()