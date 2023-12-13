import os

fileDocPath =  '/home/luohong/coding/java/github_self/back-end/docs/'
folderList = ['back-end-basic','middleware','spring','microservices','database']
lowerLevelDict = {
    'back-end-basic' : ['java集合', 'java流', 'java线程','java网络','jvm'],
    'middleware': ['redis', 'kafka', 'rocketmq', 'ShardingJDBC', '分布式调度'],
    'spring': ['spring源码', 'SpringBoot源码', 'Spring整合第三方框架'],
    'microservices': ['SpringCloud走读', 'SpringCloudAlibaba走读','分布式理论','微服务理论'],
    'database': ['mysql' ,'oltp' , 'olap', 'mpp']
}

mdFilesDict = {
    'java集合' : ['ArrayList', 'LinkedList' , 'Vector' ,'ArrayDeque' , 'HashMap', 'Hashtable' , 'LinkedHashMap' ,'WeakHashMap',
                 'ArrayBlockingQueue', 'ConcurrentHashMap', 'ConcurrentLinkedDeque', 'ConcurrentSkipListMap',
                 'ConcurrentSkipListSet','CopyOnWriteArrayList','CopyOnWriteArraySet'
                 'DelayQueue','LinkedBlockingDeque','LinkedBlockingQueue','PriorityBlockingQueue'],
    'java流' : ['零拷贝' , '输入流', '输出流'],
    'java线程' : ['thread', 'threadLocal', 'Atomic系列', 'AbstractQueuedSynchronizer' , 'ReentrantLock',
                 'ReentrantReadWriteLock', 'StampedLock', 'CountDownLatch', 'CyclicBarrier', 'ForkJoinPool',
                 'ThreadPoolExecutor', 'synchronized', 'volatile' , 'cas' , 'CHL队列' ,'Disruptor',
                 'java内存模型'],
    'java网络' : ['socket', 'tcp-udp', 'rpc'],
    'jvm' : ['jvm基础', 'jvm内存结构', 'jvm对象创建的过程', '类加载器', '垃圾回收', '逃逸分析、栈上分配、标量替换、同步消除 、内联',
             '直接内存', 'jvm监控及排查'],
    'redis' : [ 'redis为什么快', 'redis内存淘汰策略', 'redis数据结构' , 'redis持久化机制和存储原理' , 'redis主从,集群架构' , '大key问题'],
    'kafka' : [ 'kafka为什么快' , 'kafka整体架构' , 'kafka零拷贝策略', 'kafka生产者机制' , 'kafka消费者机制' , 'kafka事务' ,'kafka集群同步数据机制' ],
    'rocketmq' : [ 'rocketmq为什么快' , 'rocketmq架构' , 'rocketmq一致性事务' ],
    'ShardingJDBC' : [ 'ShardingJDBC原理' , 'ShardingJDBC实操' , 'ShardingJDBC带来的问题' ],
    '分布式调度' : ['xxl-job', 'elastic-job', 'quartz'],
    'spring源码' : ['spring源码阅读'],
    'SpringBoot源码' : ['SpringBoot源码阅读'],
    'Spring整合第三方框架' : ['Spring-MyBatis整合源码阅读'],
    'SpringCloud走读' : ['SpringCloud组件', 'Eureka阅读' , 'Feign阅读'],
    'SpringCloudAlibaba走读' : ['Nacos阅读'],
    '分布式理论' : ['cpa理论'],
    '微服务理论' : ['微服务理论'],
    'mysql' : ['mysql基础', 'mysql锁' , 'msyql索引', 'mvcc和read_view' , 'buffer_pool', 'mysql三大日志', 'mysql主从',
               'mysql执行一条sql过程'],
    'oltp' : ['oltp型数据库'],
    'olap' : ['olap分析型数据库'],
    'mpp' : ['mpp型数据库']
}


def createFolder():
    for index,value in enumerate(folderList):
        if not os.path.isdir(fileDocPath+value):
            os.makedirs(fileDocPath+value)

def createLowerLevelDict():
    for index,value in enumerate(folderList):
        lowerLevelList = lowerLevelDict[value]
        for lIndex,lValue in enumerate(lowerLevelList):
            lowerLeveFile = fileDocPath + value + '/' + lValue
            if not os.path.isdir(lowerLeveFile):
                os.makedirs(lowerLeveFile)

def createMarkDownDict():
    # /home/luohong/coding/java/github_self/back-end/docs/
    allMdDict = {}
    everyTypeDict = {}
    for index,value in enumerate(folderList):
        lowerLevelList = lowerLevelDict[value]
        for lIndex,lValue in enumerate(lowerLevelList):
            allMdDict[fileDocPath + value + '/' + lValue] = mdFilesDict[lValue]
            
            everyTypeDict[value + '/' + lValue]  = value + '/' + lValue
            #lValueList = everyTypeDict.get(lValue,[])
            #lValueList.append('/'+value + '/' + lValue + '.md')
            #everyTypeDict[lValue] = lValueList
    for key ,value in allMdDict.items():
        for index,iValue in enumerate(value):
            #print(key + '/' + iValue + '.md')      
            mdFilePath = key + '/' + iValue + '.md'
            if not os.path.exists(mdFilePath):
                file = open(mdFilePath,'w')
                file.close()
                print(mdFilePath)
            newKey = key.replace('/home/luohong/coding/java/github_self/back-end/docs','')
            #print("'"+newKey + '/' + iValue + '.md' + "',")

if __name__ == '__main__':
    #createFolder()
    #createLowerLevelDict()
    createMarkDownDict()