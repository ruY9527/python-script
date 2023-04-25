#从selenium导入浏览器驱动
from selenium import webdriver
#导入浏览器驱动设置选项
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#导入网页解析库
# from bs4 import BeautifulSoup
#导入时间库,利用time.time()防止爬虫访问过于频繁被禁止访问
import time
#导入pandas数据分析库,生成dataframe
import pandas as pd
import json


def get_cookies():
    # 对浏览器进行设置
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])  # webdriver防检测
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-dev-usage")
    option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    # 初始化谷歌浏览器
    driver = webdriver.Chrome(options=option)
    driver.set_page_load_timeout(15)
    driver.delete_all_cookies()
    url = "https://www.qichacha.com/user_login"

    driver.get(url)
    print('请在15秒内扫码登录！！！')
    time.sleep(15)
    driver.refresh()
    
    time.sleep(1)
    
    cookies = driver.get_cookies()
    print('cookies 信息')
    print(type(cookies))
    print(cookies)
    listJsonToStr(cookies)
    print('登录成功,cookies获取成功！')
    print('-'*28)
    #driver.quit()                 
    return cookies

def get_basic_info(cookies):
    """
    @ 获取企业基本信息：如法人代表、统一社会信用代码等。
    """
    driver = webdriver.Chrome()
    #下方被注释的代码可静默运行浏览器，不会显示页面，仅在后台运行
    #options=Options()
    #options.add_argument('--headless')
    #driver = webdriver.Chrome(options=options)


    driver.get("https://www.qcc.com/")
    time.sleep(1)
    '''设置cookies'''
    # cookies = cookies

    for cookie in cookies:
        print(type(cookie))
        driver.add_cookie(cookie)   #将cookies添加到浏览器
    driver.refresh()                #自动刷新页面，请检查是否已经自动登录账号
    print('加载cookies成功！')
    #driver.get("https://www.qcc.com/web/search/advance")
    #time.sleep(15)
    time.sleep(5)
    try:
        #print('开始查询')
        #driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[4]/div[1]/div[2]/div[2]/a").click()
        driver.get("https://www.qcc.com/web/search/advancelist?filter=%7B%22r%22%3A%5B%7B%22pr%22%3A%22GS%22,%22cc%22%3A%5B620900%5D%7D%5D%7D")
        #print("开始点击1111")
        #driver.findElement(By.xpath,"//a/u[contains(text(),'查一下']").click()
        #print("点击完毕222")
        #driver.switch_to.window(driver.window_handles[-1])
        time.sleep(30)
    except:
        pass
    time.sleep(5000)

    #try:
    #    driver.find_element(By.XPATH,'//*[@id="searchKey"]').send_keys(company)  #寻找输入框，输入要查询的企业名称c
    #    time.sleep(1)
    #except:
    #    raise ValueError('输入框定位/输入公司名称失败！')

    #try:
    #    driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/section[1]/div/div/div/div[1]/div/div/span/button").click() #模仿浏览器点击搜索按钮
    # bs = BeautifulSoup(driver.page_source,'html.parser')  #将加载好的网页用BeautifulSoup解析成文本
    #except:
    #    raise ValueError('定位发送按钮失败!')
    #try:
    #    tag = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div[3]/div/div[2]/div/table/tr[1]/td[3]/div/div[2]/span[1]/a')
    #    tag.click()
    #except:
    #    raise ValueError('未搜索到该公司！')

    for key,value in save_dic.items():

        save_dic[key] = [value]

    return pd.DataFrame(save_dic)

def listJsonToStr(cookies):
    fileName = 'cookies.json'
    with open(fileName, 'w', encoding='utf-8') as file_obj:
        listJson = json.dumps(cookies, ensure_ascii=False)
        file_obj.write(listJson)

def readCookieFromJson():
    fileName = 'cookies.json'
    with open(fileName, encoding='utf-8') as a:
        cookies = json.load(a)
        return cookies

if __name__ == '__main__':
    
    companies = ['华为']
    #get_cookies()
    cookies =  readCookieFromJson()
    for i in range(0,len(cookies)):
        print(type(cookies[i]))
    get_basic_info(cookies)
    #cookies = readCookieFromJson()
    #print(type(cookies))
    #cookies = [{'domain': 'www.qcc.com', 'expiry': 1698032585, 'httpOnly': False, 'name': 'CNZZDATA1254842228', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '370295421-1682305011-%7C1682305011'}, {'domain': '.qcc.com', 'expiry': 1716867767, 'httpOnly': False, 'name': 'qcc_did', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '414b2b14-711d-4536-809b-b622ade35dfa'}, {'domain': '.qcc.com', 'expiry': 1682912571, 'httpOnly': True, 'name': 'QCCSESSID', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '84dbd602e140a9f6a6811be91f'}, {'domain': '.qcc.com', 'expiry': 1698032568, 'httpOnly': False, 'name': 'UM_distinctid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '187b15b5f141107-03ad67a555854d-26031b51-1fa400-187b15b5f1513c3'}, {'domain': 'www.qcc.com', 'expiry': 1682309563, 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '717165a816823077637405495e1ff5ebcbf9a73e06667405032e78504c'}]
    #listJsonToStr(cookies)
    #print(type(companies))
    #df_basic_info = get_basic_info(company='华为')
    #new_cookies = get_cookies()
    #df_basic_info = get_basic_info(company='华为',cookies=new_cookies)