def function(param):
    return "This is my function ---> " + param

def functions1(param1,param2):
    param1 = param1 * 3
    param2 = param2 * 2 + 20
    return param1,param2

def callFunction():
    result = function('BaoYang')
    print(result)

def callManyParamFunc():
    p1,p2 = functions1(4,5)
    print(p1)
    print(p2)

if __name__ == '__main__':
    callManyParamFunc()