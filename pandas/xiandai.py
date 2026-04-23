import numpy as np
vec1 = [1,2,3,4]
vec2 = [5,6,7,8]

def distanctCos():
    dist1 = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    print("余弦距离测试结果是： \t" + str(dist1))

if __name__ == '__main__':
    distanctCos()