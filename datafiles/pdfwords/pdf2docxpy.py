import os
from pdf2docx import Converter

# 单个pdf转换为word
def pdf_docx():
    pdf_name = 'F:\\专利业务办理系统客户端.pdf'
    docx_name = 'F:\\1.doc'
    cv = Converter(pdf_name)
    cv.convert(docx_name)
    cv.close()


def pdf_list_docx(file_list_path):
    files = []
    for file in os.listdir(file_list_path):
        if file.endswith(".pdf"):
            files.append(file_list_path + "\\" +file)

    for index,file_name in enumerate(files):
        a = Converter(file_name)
        a.convert(file_name.split('.')[0] + '.docx')
        a.close()
        print(file_name + '转换成功')


if __name__ == '__main__':
    pdf_docx("E:\\学习资料\\学习资料\\讲义")