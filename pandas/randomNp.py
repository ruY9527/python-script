import numpy as np




def randomDataByNp():
    data = {
        i : np.random.randn() for i in range(7)
    }
    print(data)

def splitTup():
    tup = (4,5,6)
    # 拆分元组
    a,b,c = tup
    seq = [(1,2,3),(4,5,6),(7,8,9)]
    for a,b,c in seq:
        print('a = {0},b={1},c={2}'.format(a,b,c))

if __name__ == '__main__':
    splitTup()