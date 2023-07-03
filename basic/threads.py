#!/usr/bin/python3

import _thread
import time
import threading

exitFlag = 0

class myThread(threading.Thread):
    def __init__(self,threadId,name,delay):
        threading.Thread.__init__(self)
        self.threadId= threadId
        self.name = name
        self.delay = delay
    
    def run(self):
        print("---开始线程---" + self.name)
        

def printTimeByThread(threadName,delay,counter):
    while counter:
        if exitFlag:
            threadName.exit()
        thread.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

def printTime(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

def createThreads():
    try:
        _thread.start_new_thread(printTime, ("thread-1", 2))
        _thread.start_new_thread(printTime, ("thread-2", 4))
    except:
        print("捕获到错误")


if __name__ == '__main__':
    #createThreads()
    # 卡顿,别让线程终止
    #while 1:
    #    pass
    thread11 = myThread(1, "thread-1", 1)
    thread22 = myThread(2, "thread-2", 2)

    thread11.start()
    thread22.start()

    thread11.join()
    thread22.join()
    print("----- 退出主线程 ------")


