#!/usr/bin/python3


def basicLambdaUse():
    x = lambda a : a + 10
    print(x(5))

    sum = lambda args1,args2 : args1 + args2
    print(sum(15,9))


if __name__ == '__main__':
    basicLambdaUse()