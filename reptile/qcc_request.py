# 企查查请求数据


import requests

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'sec-ch-ua':'"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"Windows"',
    'sec-fetch-dest':'document',
    'sec-fetch-mode':'navigate',
    'sec-fetch-site':'same-origin',
    'cookie': 'QCCSESSID=c79470230f4ebf2220bde31526; qcc_did=a161c896-db5b-4be8-8cc7-075ee71b72cc; UM_distinctid=187acc6c8ae12a-03a541bd06547e-6701434-1fa400-187acc6c8afae0; acw_tc=7250b39916822985713744813e7602ba9662715ea391f5cc7b55823713; CNZZDATA1254842228=2056543923-1682229410-%7C1682298745'
}
url = 'https://www.qcc.com/web/search/advancelist?filter=%7B%22r%22%3A%5B%7B%22pr%22%3A%22GS%22,%22cc%22%3A%5B620900%5D%7D%5D%7D'
response = requests.get(url, headers=headers)
response.encoding = response.apparent_encoding
print(response.text)
print(response)
