import os
from pdf2docx import Converter
 
def pdf_docx():
 
    # 获取当前工作目录
    #file_path = os.getcwd()
 
    # 获取所有文件
    #files = os.listdir(file_path)
 
    # 遍历所有文件
    #for file in files:
 
    # 过滤临时文件
    #if '~$' in file:
    #    continue

    # 过滤非pdf格式文件
    #if file.split('.')[-1] != 'pdf':
    #    continue
    # 获取文件名称
    #file_name = file.split('.')[0]
    pdf_name = 'F:\\专利业务办理系统客户端.pdf'
    docx_name = 'F:\\1.doc'
    # pdf文件名称
    #pdf_name = os.getcwd() + '\\' + file
    # docx文件名称
    #docx_name = os.getcwd() + '\\' + file_name + '.docx'
    # 加载pdf文档
    cv = Converter(pdf_name)
    # cv.convert(docx_name, start=0, end=12)
    cv.convert(docx_name)
    cv.close()

if __name__ == '__main__':
    pdf_docx()