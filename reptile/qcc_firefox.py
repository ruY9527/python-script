#coding=utf-8

import os
from selenium import webdriver
import time


# C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\xr10j3j7.default
#profileDir = 'C:\\Users\\Administrator\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xr10j3j7.default'
#profile = webdriver.FirefoxProfile(profileDir)
# cookie_url = 'https://www.qcc.com/'

driver  = webdriver.Firefox()
driver.get('https://www.qcc.com/')
time.sleep(3)
cookies = driver.get_cookies()
print('获取cookie信息')
print(cookies)
print("-----------")
driver.refresh()
time.sleep(500)