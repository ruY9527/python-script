import heapq
from collections import OrderedDict

def getMaxMinNum():
    dataList = [
        {'S': 5, 'H': 3}, 
        {'S': 7, 'H': 1}, 
        {'S': 0, 'H': 2}
    ]
    d = heapq.nlargest(1,dataList,key=lambda x:x['S'])
    print(d)

def sortByHeadq():
    k = [2, 6, 1, 5, 3, 4]
    kSortList = heapq.nsmallest(len(k),k)
    print(kSortList)
    
    nameList = ['LG', 'cdn', 'dll', 'BBQ', 'afun']
    xLambda = lambda x: (len(x),x)
    nameSortList = sorted(nameList,key=xLambda)
    print(nameSortList)

def sortDict():
    d = {'apple': 1, 'orange': 3, 'banana': 4, 'tomato': 2}
    dDict = OrderedDict((x,y) for x,y in sorted(d.items(),key=lambda x:x[1]))
    print(dDict)

def mergeDict():
    d1 = {'a': 1}
    d2 = {'b': 2}
    #d1.update(d2)
    #d = dict(d1,**d2)
    d = { **d1, **d2 }
    print(d)
    

if __name__ == '__main__':
    mergeDict()

