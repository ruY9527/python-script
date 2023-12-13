#coding=utf-8

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


# 读取 avro 文件
def readAvroFile(fileLocation):
    all_dict_list = []
    reader = DataFileReader(open(fileLocation, "rb"), DatumReader())
    for user in reader:
        print(user)
        print(type(user))
        all_dict_list.append(user)
    reader.close()
    print(len(all_dict_list))


if __name__ == '__main__':
    readAvroFile("F:\\3.avro")
    