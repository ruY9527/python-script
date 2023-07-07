#!/usr/bin/python3
from functools import reduce

arr = [1, 2, 3, 4, 5, 6, 7, 8]

def square(x):
    return x*x
result = map(square,arr)

def forIt():
    result1 =  [ x*x for x in arr if x >= 4 ]
    print(list(result1))

def basicLambdaUse():
    x = lambda a : a + 10
    print(x(5))

    sum = lambda args1,args2 : args1 + args2
    print(sum(15,9))

def reducebase():
    rResult = reduce(lambda x,y : x + y, arr)
    print(rResult)

def filterBase():
    fResult = filter(lambda x:True if x==1 else False, arr)
    print(list(fResult))


if __name__ == '__main__':
    #print(list(result))
    filterBase()