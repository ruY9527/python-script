import PyPDF4
import pikepdf
import fitz

def pdf_image(pdf_name):
    doc = fitz.open("E:\\pdfs\\labelPrint (3).pdf")
    reader = PyPDF4.PdfFileReader('E:\\pdfs\\labelPrint (3).pdf')
    pageNum = reader.getNumPages()
    for pg in range(0,pageNum):
        page = doc.load_page(pg)
        pix = page.get_pixmap()
        a = str(pg)
        b = 'E:\\pdfs\\'
        c = ".png"
        pix.save(b+a+c)
 
## 需要先安装  fitz ; 再按照PyMuPDF
if __name__ == '__main__':
    # E:\pdfs\labelPrint (3).pdf
    pdf_image('E:\\pdfs\\labelPrint (3).pdf')
    