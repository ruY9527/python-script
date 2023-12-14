#coding=utf-8

import aspose.words as aw

# 单个文件的转换
def oneFileConver():
    doc = aw.Document(r"‪E:\学习资料\学习资料\讲义\1.1 计算机系统简介.pdf")
    doc.save("‪E:\学习资料\学习资料\讲义\Output.md")

if __name__ == '__main__':
    oneFileConver()
