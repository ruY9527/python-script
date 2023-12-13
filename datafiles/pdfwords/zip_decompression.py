import zipfile,os


# 解压zip包文件夹
def file_to_zip_list(zip_path):
    #当前路径
    os.getcwd()
    #转到路径
    os.chdir(zip_path)
    file_list = []
    for file_path,sub_dirs,files in os.walk(zip_path):
        file_list = files
    
    for index,file_name in enumerate(file_list):
        if file_name.endswith('zip'):
            all_path = zip_path + "\\" + file_name
            print(file_name)
            r = zipfile.is_zipfile(file_name)
            if r:
                zpfd = zipfile.ZipFile(file_name)
                os.chdir(zip_path)
                zpfd.extractall()
                zpfd.close()
                os.chdir(zip_path)

def delete_file_with_end(zip_path):
    pass

if __name__ == '__main__':
    #file_to_zip_list('F:\\2022\\1-6\\1-6')
    file_to_zip_list('F:\\2022\\7-12\\7-12')