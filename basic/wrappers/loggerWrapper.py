import time

def logger(func):
    def wrapper(*args,**kw):
        print('我准备开始计算：{} 函数了:'.format(func.__name__))
        func(*args, **kw)
        print('我准备开始计算：{} 函数了:'.format(func.__name__))
    return wrapper

def timer(func):
    def wrapper(*args,**kw):
        t1 = time.time
        func(*args,**kw)
        t2 = time.time()
        cost_time = t2 - t1
        print("花费时间：{}秒".format(cost_time))
    return wrapper

class loggerFunc(object):
    def __init__(self,func):
        self.func = func

    def __call__(self,*args,**kwargs):
        print("[INFO]: the function {func}() is running....".format(func=self.func.__name__))
        return self.func(*args, **kwargs)

@loggerFunc
def say(something):
    print("say {} !".format(something))

@logger
def add(x,y):
    print('{} + {} = {}'.format(x, y, x+y))

@timer
def want_sleep(sleep_time):
    time.sleep(sleep_time)


if __name__ == '__main__':
    add(1,2)
    say("hello world~!~~")
    want_sleep(5)
