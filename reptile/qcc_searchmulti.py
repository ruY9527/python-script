#coding=utf-8
# author：墨雨微晴
# date：2023/01/16
# note：企查查批量查询接口，可以获取多条企业信息，且速度较快
# note：需要填写自己的账号cookie，且最大的单次爬取数量取决于自己的账号等级，如vip为5000条，svip为10000条

import requests
import json
import re
import os
import hmac
import time
import hashlib
import datetime
import logging
import pandas as pd
import math

# user_cookie
# 用户cookie，填写自己的用户cookie
cookie = 'qcc_did=20441bc6-d10a-4f98-89d4-17ef13453b03; UM_distinctid=186d8c98b67b54-07f958b5e5fc51-26031851-1fa400-186d8c98b68101b; QCCSESSID=d35df13ab54709aab171120bca; _uab_collina=168232751304679793184927; acw_tc=717165aa16823859330943589e600f4558b48d92be35b84613c7744c30; CNZZDATA1254842228=204211623-1678672691-https%253A%252F%252Fwww.baidu.com%252F%7C1682384216'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
request_data_dict = dict()
request_data_dict['jq_data'] = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}]}","pageSize":20,"isAgg":"false","isLimit":False}
request_data_dict['individuality_data'] = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}],\"ot\":[\"001009\"]}","pageSize":20,"isAgg":"false","isLimit":False}
request_data_dict['enterprise_data'] = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}],\"ot\":[\"001001001\",\"001001002\",\"001007\",\"001002001\",\"001002002\",\"001002003\",\"001002004\",\"001006\"]}","pageSize":20,"isAgg":"false","isLimit":False}
request_data_dict['innovative_data'] = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}],\"tec\":[\"T_INNMS\"]}","pageSize":20,"isAgg":"false","isLimit":False}
request_data_dict['specialized'] = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}],\"tec\":[\"SSE\",\"T_SSTE\"]}","pageSize":20,"isAgg":"false","isLimit":False}
request_data_dict['financing'] = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}],\"rl\":[\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"8\",\"9\",\"10\",\"11\"]}","pageSize":20,"isAgg":"false","isLimit":False}

def get_pid_tid():
    url = 'https://www.qcc.com/web/search/advance?hasState=true'

    headers = {
        'accept-encoding': 'gzip, deflate, br'
        ,'accept-language': 'zh-CN,zh;q=0.9'
        ,'cache-control': 'max-age=0'
        ,'cookie' : cookie
        ,'referer': 'https://www.qcc.com/'
        ,'sec-fetch-dest': 'document'
        ,'sec-fetch-mode': 'navigate'
        ,'sec-fetch-site': 'same-origin'
        ,'sec-fetch-user': '?1'
        ,'upgrade-insecure-requests': '1'
        ,'user-agent': user_agent
    }

    res = requests.get(url, headers=headers).text
    try:
        pid = re.findall("pid='(.*?)'", res)[0]
        tid = re.findall("tid='(.*?)'", res)[0]
    except:
        pid = ''
        tid = ''

    return pid, tid

def honor_pid_tid(eid):
    url = "https://www.qcc.com/creport/" + eid + ".html"
    headers = {
         'accept-encoding': 'gzip, deflate, br'
        ,'accept-language': 'zh-CN,zh;q=0.9'
        ,'cache-control': 'max-age=0'
        ,'cookie' : cookie
        ,'sec-fetch-dest': 'document'
        ,'sec-fetch-mode': 'navigate'
        ,'sec-fetch-site': 'same-origin'
        ,'sec-fetch-user': '?1'
        ,'upgrade-insecure-requests': '1'
        ,'user-agent': user_agent
    }
    print("the url is ---> " + url)
    res = requests.get(url,headers = headers).text
    print(res)
    try:
        pid = re.findall("pid='(.*?)'", res)[0]
        tid = re.findall("tid='(.*?)'", res)[0]
    except:
        pid = ''
        tid = ''

    return pid, tid

def financing_pid_tid(eid):
    url = "https://www.qcc.com/firm/" + eid + ".html"
    headers = {
         'accept-encoding': 'gzip, deflate, br'
        ,'accept-language': 'zh-CN,zh;q=0.9'
        ,'cache-control': 'max-age=0'
        ,'cookie' : cookie
        ,'sec-fetch-dest': 'document'
        ,'sec-fetch-mode': 'navigate'
        ,'sec-fetch-site': 'same-origin'
        ,'sec-fetch-user': '?1'
        ,'upgrade-insecure-requests': '1'
        ,'user-agent': user_agent
    }
    print("the url is ---> " + url)
    res = requests.get(url,headers = headers).text
    print(res)
    try:
        pid = re.findall("pid='(.*?)'", res)[0]
        tid = re.findall("tid='(.*?)'", res)[0]
    except:
        pid = ''
        tid = ''

    return pid, tid

def seeds_generator(s):
    seeds = {
        "0": "W",
        "1": "l",
        "2": "k",
        "3": "B",
        "4": "Q",
        "5": "g",
        "6": "f",
        "7": "i",
        "8": "i",
        "9": "r",
        "10": "v",
        "11": "6",
        "12": "A",
        "13": "K",
        "14": "N",
        "15": "k",
        "16": "4",
        "17": "L",
        "18": "1",
        "19": "8"
    }
    seeds_n = 20

    if not s:
        s = "/"
    s = s.lower()
    s = s + s

    res = ''
    for i in s:
        res += seeds[str(ord(i) % seeds_n)]
    return res

def a_default(url: str = '/', data: object = {}):
    url = url.lower()
    dataJson = json.dumps(data, ensure_ascii=False, separators=(',', ':')).lower()

    hash = hmac.new(
        bytes(seeds_generator(url), encoding='utf-8'),
        bytes(url + dataJson, encoding='utf-8'),
        hashlib.sha512
    ).hexdigest()
    return hash.lower()[8:28]

def r_default(url: str = '/', data: object = {}, tid: str = ''):
    url = url.lower()
    dataJson = json.dumps(data, ensure_ascii=False, separators=(',', ':')).lower()

    payload = url + 'pathString' + dataJson + tid
    key = seeds_generator(url)

    hash = hmac.new(
        bytes(key, encoding='utf-8'),
        bytes(payload, encoding='utf-8'),
        hashlib.sha512
    ).hexdigest()
    return hash.lower()


def make_request(data, pid, tid):
    url = 'https://www.qcc.com/api/search/searchMulti'
    headers = {
        'accept': 'application/json, text/plain, */*'
        ,'accept-encoding': 'gzip, deflate, br'
        ,'accept-language': 'zh-CN,zh;q=0.9'
        ,'content-length': '141'
        ,'content-type': 'application/json'
        ,'origin': 'https://www.qcc.com'
        ,'cookie' : cookie
        ,'referer': 'https://www.qcc.com/web/search/advance?hasState=true'
        ,'sec-fetch-dest': 'empty'
        ,'sec-fetch-mode': 'cors'
        ,'sec-fetch-site': 'same-origin'
        ,'user-agent': user_agent
        ,'x-requested-with': 'XMLHttpRequest'
    }

    headers['x-pid'] = pid

    req_url = '/api/search/searchmulti'

    key = a_default(req_url, data)
    val = r_default(req_url, data, tid)
    headers[key] = val

    res = requests.post(url=url, headers=headers, json=data).text
    res_json = json.loads(res)
    return res_json

def honor_request(eid,data,pid,tid):
    url = 'https://www.qcc.com/api/datalist/teclist'
    headers = {
        'accept': 'application/json, text/plain, */*'
       ,'accept-encoding': 'gzip, deflate, br'
       ,'accept-language': 'zh-CN,zh;q=0.9'
       ,'content-length': '110'
       ,'content-type': 'application/json'
       ,'cookie': cookie
       ,'referer': 'https://www.qcc.com/creport/' + eid + ".html"
       ,'sec-fetch-dest': 'empty'
       ,'sec-fetch-mode': 'cors'
       ,'sec-fetch-site': 'same-origin'
       ,'user-agent': user_agent
       ,'x-requested-with': 'XMLHttpRequest'
    }
    headers['x-pid'] = pid
    req_url = '/api/datalist/teclist'
    key = a_default(req_url, data)
    val = r_default(req_url, data, tid)
    headers[key] = val
    res = requests.post(url=url, headers=headers, json=data).text
    res_json = json.loads(res)
    return res_json

def financing_request(eid,f_url,pid,tid):
    data = {}
    req_url = f_url
    url = 'https://www.qcc.com' + f_url
    headers = {
        'accept': 'application/json, text/plain, */*'
       ,'accept-encoding': 'gzip, deflate, br'
       ,'accept-language': 'zh-CN,zh;q=0.9'
       ,'content-type': 'application/json'
       ,'cookie': cookie
       ,'referer': 'https://www.qcc.com/creport/' + eid + ".html"
       ,'sec-fetch-dest': 'empty'
       ,'sec-fetch-mode': 'cors'
       ,'sec-fetch-site': 'same-origin'
       ,'user-agent': user_agent
       ,'x-requested-with': 'XMLHttpRequest'
       ,'x-function-name': '%E8%9E%8D%E8%B5%84%E4%BF%A1%E6%81%AF'
    }
    headers['x-pid'] = pid
    
    key = a_default(req_url, data)
    val = r_default(req_url, data, tid)
    headers[key] = val
    print("url ---> " + url)
    print(headers)
    res = requests.get(url=url, headers=headers).text
    res_json = json.loads(res)
    return res_json

def simpleFunction():
    pid, tid = get_pid_tid()
    enterinfo_list = []
    honor_req_data = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}],\"tec\":[\"SSE\",\"T_SSTE\"]}","pageSize":20,"isAgg":"false","isLimit":False}
    #honor_req_data = {"filter":"{\"r\":[{\"pr\":\"GS\",\"cc\":[620900]}],\"rl\":[\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"8\",\"9\",\"10\",\"11\"]}","pageSize":20,"isAgg":"false","isLimit":False}
    resp_json = make_request(honor_req_data,pid,tid)
    total_count = resp_json.get('Paging').get('TotalRecords')
    result_data_list = resp_json.get('Result')
    for index,value in enumerate(result_data_list):
        one_enterprise_dict = dict()
        one_enterprise_dict['KeyNo'] = value.get('KeyNo')
        one_enterprise_dict['Name'] = value.get('Name')
        one_enterprise_dict['CreditCode'] = value.get('CreditCode')
        enterinfo_list.append(one_enterprise_dict)
    #print(math.ceil(43/20))
    if total_count > 20:
        pageCounts = math.ceil(total_count / 20) + 1
        for index in range(2,pageCounts):
            honor_req_data['pageIndex'] = index
            many_resp_json = make_request(honor_req_data,pid,tid)
            many_result_list = many_resp_json.get('Result')
            for mIndex,mValue in enumerate(many_result_list):
                m_one_enterprise_dict = dict()
                m_one_enterprise_dict['KeyNo'] = mValue.get('KeyNo')
                m_one_enterprise_dict['Name'] = mValue.get('Name')
                m_one_enterprise_dict['CreditCode'] = mValue.get('CreditCode')
                enterinfo_list.append(m_one_enterprise_dict)
    listJsonToStr('honor.json',enterinfo_list)

def get_honor_data():
    honor_enterprise_list = readCookieFromJson('honor.json')
    honor_data_list = []
    for index,value in enumerate(honor_enterprise_list):
        eid = value.get('KeyNo')
        pid,tid = honor_pid_tid(eid)
        if pid == '' or tid == '':
            break
        request_data = { "keyNo" : eid }
        print('pid ---> ' + pid + "   :  tid ---> " + tid)
        print(request_data)
        honor_resp =  honor_request(eid,request_data,pid,tid)
        print('eid: ' + eid)
        honor_resp_data = honor_resp.get('data')
        for hIndex,hValue in enumerate(honor_resp_data):
            honor_dict = dict()
            honor_dict['Name'] = value.get('Name')
            honor_dict['CreditCode'] = value.get('CreditCode')
            honor_dict['DirectoryName'] = hValue.get('DirectoryName')
            honor_dict['CertificateCode'] = hValue.get('CertificateCode')
            honor_dict['KindDesc'] = hValue.get('KindDesc')
            honor_dict['ApproveClassDesc'] = hValue.get('ApproveClassDesc')
            honor_dict['Title'] = hValue.get('Title')
            honor_dict['PublishOffice'] = hValue.get('PublishOffice')
            honor_dict['PublishDate'] = hValue.get('PublishDate')
            honor_dict['LastestBegingDate'] = hValue.get('LastestBegingDate')
            honor_dict['LatestDeadLine'] = hValue.get('LatestDeadLine')
            honor_data_list.append(honor_dict)
        time.sleep(3)
    listJsonToStr('honor_data.json',honor_data_list)

def listJsonToStr(fileName,honor_list):
    #fileName = 'honor.json'
    with open(fileName, 'w', encoding='utf-8') as file_obj:
        listJson = json.dumps(honor_list, ensure_ascii=False)
        file_obj.write(listJson)

def readCookieFromJson(fileName):
    #fileName = 'cookies.json'
    with open(fileName, encoding='utf-8') as a:
        cookies = json.load(a)
        return cookies

if __name__ == '__main__':
    #simpleFunction()
    #pid, tid = get_pid_tid()
    #print('pid : ' + pid)
    #print('tid : ' + tid)
    # 市场主体   个体工商户   企业数量   创新型中小企业数量
    #requests_counts = ['jq_data', 'individuality_data' , 'enterprise_data' , 'innovative_data']
    #for index in range(len(requests_counts)):
    #    request_data = request_data_dict.get(requests_counts[index])
    #    resp_json = make_request(request_data, pid, tid)
    #    result_count = resp_json.get('Paging').get('TotalRecords')
    #    print(str(index + 1 ) + " : 个数" + str(result_count))

    
    financing_enterprise_list = readCookieFromJson('financing.json')
    financing_data_list = []
    for index,value in enumerate(financing_enterprise_list):
        eid = value.get('KeyNo')
        pid,tid = financing_pid_tid(eid)
        url = '/api/datalist/financinginfo?key=' + eid + "&pageSize=100&searchKey="+eid+"&searchType=ckw&sortField=date"
        resp = financing_request(eid,url,pid,tid)
        resp_data = resp.get('data')
        for fIndex,fValue in enumerate(resp_data):
            f_dict = dict()
            f_dict['Date'] = fValue.get('Date')
            f_dict['ProductName'] = fValue.get('ProductName')
            f_dict['Round'] = fValue.get('Round')
            f_dict['Valuation'] = fValue.get('Valuation')
            f_dict['Amount'] = fValue.get('Amount')
            f_dict['NewsUrl'] = fValue.get('NewsUrl')
            f_dict['Name'] = value.get('Name')
            f_dict['CreditCode'] = value.get('CreditCode')
            financing_data_list.append(f_dict)
        time.sleep(5)
    listJsonToStr('financing_data.json',financing_data_list)
    #for index,value in enumerate(honor_enterprise_list):
    #eid = value.get('KeyNo')
    #eid = '7d9d21e5d830c512682d8a75f51f8ade'
    #pid,tid = financing_pid_tid(eid)
    #print('pid ---> ' + pid + "   :  tid ---> " + tid)
    #url = '/api/datalist/financinginfo?keyNo=7d9d21e5d830c512682d8a75f51f8ade&pageSize=100&searchKey=7d9d21e5d830c512682d8a75f51f8ade&searchType=ckw&sortField=date'
    #resp = financing_request(eid,url,pid,tid)
    #print(resp)
    
            #sprint(index)
    # 获取荣誉信息
    #pid, tid = honor_pid_tid('fefb1a5fbc7e7ad1e0d925fc0e2e593e');
    #print("pid: " + pid + " ---- tid: " + tid)
    # data = {"keyNo":"fefb1a5fbc7e7ad1e0d925fc0e2e593e","relatedSec":"f03feaa17edf4fe2b19c2eb90d73db74","symbol":"831985"}
    #data = {"keyNo" : "fefb1a5fbc7e7ad1e0d925fc0e2e593e"}
    #honor_resp = honor_request('fefb1a5fbc7e7ad1e0d925fc0e2e593e', data, pid, tid)
    #print(honor_resp.get('data'))
    #honor_request()
    #print("pid: " + pid + " ---- tid: " + tid)