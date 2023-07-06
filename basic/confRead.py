import configparser


def confReadFile():
    config = configparser.ConfigParser()
    config.read('config1.conf', encoding='utf-8')

    # 获取所有节点名字
    secs = config.sections()
    mysqlOptions = config.options('mysql')
    print(mysqlOptions)
    print(type(mysqlOptions))
    for index,value in enumerate(mysqlOptions):
        cValue = config.get('mysql', value)
        print(cValue)

def iniRead():
    config = configparser.ConfigParser()
    iniConfig = config.read('config1.ini', encoding='utf-8')   
    
    sec = config.sections()
    print(sec)
    
    opt = config.options('mysql')
    print(opt)
    
    mValue = config.items('mysql')
    for index,value in dict(mValue).items():
        print("value: " + value)
    
if __name__ == '__main__':
    iniRead()