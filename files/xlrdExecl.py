import xlrd
from datetime import date,datetime
import os
import xlwt

def xlrdApi():
    data = xlrd.open_workbook('/home/luohong/Downloads/111.xlsx')
    sheetNames = data.sheet_names()
    sheetCounts = data.nsheets
    print(sheetNames)
    print(sheetCounts)

    sheetObj = data.sheet_by_name('1')
    one_sheet_names = sheetObj.name
    one_sheet_nrows = sheetObj.nrows
    one_sheet_ncols = sheetObj.ncols
    one_sheet_rows_data = sheetObj.row_values(0)
    one_sheet_col_data = sheetObj.col_values(0)
    print(one_sheet_names)
    print(one_sheet_nrows)
    print(one_sheet_ncols)
    print(one_sheet_rows_data)
    print(one_sheet_col_data)

def writeDateByXlrd():
    book = xlwt.Workbook() # 新建工作簿
    table = book.add_sheet('Over',cell_overwrite_ok=True) # 如果对同一单元格重复操作会发生overwrite Exception，cell_overwrite_ok为可覆盖
    sheet = book.add_sheet('Test') # 添加工作页
    #sheet = book.add_sheet('Test') # 添加工作页
    sheet.write(1,1,'A')
    style = xlwt.XFStyle() # 新建样式
    font = xlwt.Font() #新建字体
    font.name = 'Times New Roman'
    font.bold = True
    style.font = font # 将style的字体设置为font
    table.write(0,0,'Test',style)
    book.save(filename_or_stream='/home/luohong/Downloads/111.xlsx') # 一定要保存
    
if __name__ == '__main__':
    writeDateByXlrd()