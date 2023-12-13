import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


# 首先定义一个解析pdf文档的函数
# 解析pdf文件，获取文件中包含的各种对象
def parse(pdf_path):
    # 这里以二进制读模式打开pdf文档
    fp = open(pdf_path, 'rb')
    # 接着用文件对象来创建一个pdf文档解析
    parser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
        num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0

        # 循环遍历列表，每次处理一个page的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 页面加1
            num_page += 1
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            for x in layout:
                # 图片对象
                if isinstance(x, LTImage):
                    num_image += 1
                    # 曲线对象
                if isinstance(x, LTCurve):
                    num_curve += 1
                # figure对象
                if isinstance(x, LTFigure):
                    num_figure += 1
                # 获取文本内容
                if isinstance(x, LTTextBoxHorizontal):
                    # 水平文本框对象加1
                    num_TextBoxHorizontal += 1
                    # 保存文本内容，生成doc文件的文件名及路径
                    with open(r'F:\\1.docx', 'a', encoding='utf-8') as f:
                        results = x.get_text()
                        f.write(results)
                        f.write('\n')

                    # 打印出paf文档的对象情况
    print('对象数量：\n', '页面数：%s\n' % num_page, '图片数：%s\n' % num_image, '曲线数：%s\n' % num_curve, '水平文本框：%s\n'
          % num_TextBoxHorizontal)


# 执行主函数
if __name__ == '__main__':
    # 读取pdf文件路径及文件名
    pdf_path = r'F:\\专利业务办理系统客户端.pdf'
    # 对该路径下的pdf文件执行上面自定义的解析pdf文档的函数
    parse(pdf_path)