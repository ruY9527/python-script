from xml.dom.minidom import parse
 

def readXmlFile():
    # 读取文件
    dom = parse('1.xml')
    # 获取文档元素对象
    data = dom.documentElement
    urlList =  data.getElementsByTagName('url')
    for url in urlList:
        locInfo = url.getElementsByTagName('loc')[0].childNodes[0].nodeValue
        print(locInfo)
    
if __name__ == '__main__':
    readXmlFile()