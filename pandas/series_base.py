#!/usr/bin/python
# coding=utf-8
import pandas as pd
import numpy as np

"""
基础创建序列化
"""
def create_series():
    series = pd.Series([1,2,3,4], name='A')
    print(series)
    custom_index = [1,2,3,4]
    series_with_index = pd.Series([1,2,3,4], index=custom_index, name='B')
    print(series_with_index)

def create_index():
    a = ["Google", "Runoob", "Wiki"]
    my_var = pd.Series(a, index=["x","y","z"])
    print(my_var)

"""
默认创建字典
"""
def create_dict():
    sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
    my_var = pd.Series(sites)
    print(my_var)

"""
基础的base相关函数调用
"""
def create_index_data_sum():
    data = [1, 2, 3, 4, 5, 6]
    index = ['a', 'b', 'c', 'd', 'e', 'f']
    s = pd.Series(data, index=index)
    print("索引：", s.index)
    print("数据：", s.values)
    print("数据类型：", s.dtype)
    print("前两行数据：", s.head(2))

    s_doubled = s.map(lambda x: x * x)
    print("元素加倍后：", s_doubled)

    cumsum_s = s.cumsum()
    print("累计求和：", cumsum_s)

    print("缺失值判断：", s.isnull())

    sorted_s = s.sort_values()
    print("排序后的 Series：", sorted_s)

def np_array():
    ndarray_data = np.array([
        ['Google', 10],
        ['Runoob', 12],
        ['Wiki', 13]
    ])
    df = pd.DataFrame(ndarray_data, columns=['Site', 'Age'])
    print(df)

def np_dict():
    data = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
    """
        a   b     c
        0  1   2   NaN
        1  5  10  20.0
    """
    df = pd.DataFrame(data)
    print(df)

def np_loc_info():
    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
    }
    df = pd.DataFrame(data)
    print(df.loc[0])
   #print(df.loc[1])


if __name__ == '__main__':
    np_loc_info()