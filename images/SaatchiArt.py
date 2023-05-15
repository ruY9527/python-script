import requests
from bs4 import BeautifulSoup
import urllib.request

# Saatchi Art 页面的 URL
url = 'https://www.saatchiart.com/paintings/oil/feature?page=2'
headers = {
    'accept-user': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cache-control':'max-age=0',
    'cookie':'User-Continent=AS; User-Country=JP; User-Region=13; User-Device-OS=Linux; saatchi_user_preferences={"country":"JP","language":"english","currency":"USD","measurementUnit":"cm","userRole":"guest"}; saatchivc=vc_nh71guvipu; saatchi_abtests=; _gid=GA1.2.283059000.1683983392; _gcl_au=1.1.276494419.1683983393; wgdpr=yes; __pdst=32e7f36abe69491abfa8f6f974ede21d; _fbp=fb.1.1683983393554.308831606; _pin_unauth=dWlkPVpEUmpOekV6TjJFdE1qZG1aUzAwTVRneUxUazVZVEl0T1RNd1ptWXpNRFZrTkRKag; tkbl_cvuuid=ddc0ae65-0d44-4b75-a696-018d4cd24505; __qca=P0-507219192-1683983393374; btIdentify=390439e0-7221-4289-92cb-412ed1889bdc; intercom-id-iqk9bu78=758bce1f-91bb-43b7-bf74-e1b2190ea878; intercom-session-iqk9bu78=; intercom-device-id-iqk9bu78=28a1870d-54e5-417c-bea5-e17384c7eb2a; tatari-session-cookie=b0c6b98c-d7c1-7311-d007-71431a4e7c5e; bluecoreNV=false; cto_bundle=LAv5N19aazBCWk1qMUR5M0l4NVpjUVFyM3Azcm5JMklKdmlGYmFudU9hJTJCNjFHMklSREg0NDRnZVRDN3lyejV5Q2pDbWRSc05zaXl6bDM3ZGc2eEEzamMlMkJiNk05OTBvTFd5eCUyRkpQRnhBcW1WWTZWRmEySlhEMEN6SCUyQm1zUGo0UHRhUXBYd3hzMVFyeFd5a0dMQjhjMlJ5VTh2ZyUzRCUzRA; bm_sv=441BDA418C421D0F505AB91FE9331A08~YAAQDS7AF/pnvAiIAQAAMuOrFRNnaxun13RMqIBV5FJ02AP+wSDHTTu3olHJr4JWWuMzMnquHTcTsto5x94DOInW26lPFOevlTQ6iWc9TBeTVdIgSFkH7Q1hrCNDUBxMPuUJEEE08UuegiM+xXXgLbRl6QZLSyzAtE30vNfQRPxVZfU3z4PuDGAajbRTjqmJngFuxnx4OpH++3HX5PreB5HIqU77I6w6tNSj1S9r0lEyhM6+meTv3+LhoO6mjqxVuJ9WeQ==~1; ak_bmsc=8C134A752907D3243F2296468921ECF1~000000000000000000000000000000~YAAQDS7AFxZovAiIAQAAduOrFRNAK+lhuNMQ+YC/IjXrIlISkkXU+mBj/BnNfr62P7X7V2DiQCxXY0tCMHS/fvNe+iHOtOmDrRl6PKi7C8Llue+l2/8SEP7RANZCe/y0cjsMsHjB+yYHLEcPL02kOeeX50HcT/6N//RLnoKzQQUD/myeXCdH+04RIJ+y+LGnX4e0GbVd9uaj13lsv/aYeAr9f8XpEt35sxxI51mDS1K42dUN+Vkjg1SEn201ZPWvRV3WyFdQ1zwxKnnXnDAlX2qbH0ornqhciyDr0fOk4Of2zHwTV+lJnPBxJXhcAKR2e6FY/2SIe1gTkjoSh6UlF1SGeVKIXaZkIW2J9YK9hmeKYLM2R1uDrsMvCQi/r0xBoOnr1/khgH6wYEOww66CFXJiD2jshTiZOg+8+OwTudCHbljQdPJjipPvqvh+8+QaEflYC0lSubGpRrZmXhrOMwkRC5zhseacmpiVVHKTYKIBFbbuMs5l73+DAzsBxso=; tatari-cookie-test=66340965; t-ip=1; OptanonConsent=isGpcEnabled=0&datestamp=Sat+May+13+2023+15:12:46+GMT+0000+(GMT)&version=202211.2.0&isIABGlobal=false&hosts=&consentId=41d05322-35e6-491f-a9b7-31939f5f0743&interactionCount=1&landingPath=NotLandingPage&groups=C0001:1,C0003:1,SPD_BG:1,C0002:1,C0004:1&AwaitingReconsent=false; _ga_550YY93L77=GS1.1.1683990765.2.1.1683990766.59.0.0; _uetsid=73624ae0f18f11ed90701b705eaaf6c6; _uetvid=73628b70f18f11ed931ea9c178a89119; mp_saatchi_art_mixpanel={"distinct_id": "188153b62c95e-073f0b39825df-17462c6c-144000-188153b62caca6","bc_persist_updated": 1683983408052,"geo": "jp"}; AMP_TOKEN=$NOT_FOUND; _ga=GA1.2.1795697962.1683983392; _dc_gtm_UA-15756294-1=1; bc_invalidateUrlCache_targeting=1683990767020; _bts=12d2846b-82c6-44d3-8886-d822684a0d86; _bti={"app_id":"saatchi-art","bsin":"R2VCDp7zK4z4fCU3PYcvUKlcRz7iGQPywAIRvEDkhfXkKwveWxcBX2nmzBF0B0PXw80uDNxXapsQmAzsyDdr5g==","is_identified":false}; _gat_gtag_UA_19048290_1=1',
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
# 发送请求获取 HTML 页面
response = requests.get(url,headers=headers)
html = response.text
# 解析 HTML 页面
soup = BeautifulSoup(html, 'html.parser')
aList = soup.find_all('picture')
print(len(aList))
image_url_list = []
for a in aList:
    a_one_img = a.find_all('img')[0]
    image_url = ''
    if a_one_img.has_attr('src'):
        image_url = a_one_img['src']
    if a_one_img.has_attr('data-src'):
        image_url = a_one_img['data-src']
    image_url_list.append(image_url)
    #print(image_url)
    #image_url_list.append(a_one_img['src'])
    #    print(type(a_one_img['src']))
    #    print(a_one_img['src'])

for i,link in enumerate(image_url_list):
    filename = link.split('/')[-1]
    #filename = f"oil_painting_{i+1}.jpg"
    rsp = requests.get(link,headers=headers)
    with open(filename, 'wb') as f:
        f.write(rsp.content)
        print(f'{filename}下载完成')
#    print(type(filename))
#    headers['Referer'] = 'https://www.saatchiart.com/paintings/oil'
#    print(link)
#    req = urllib.request.Request(link, headers=headers)
#    urllib.request.urlretrieve(req, filename)
#    print(f"下载图片 {i+1}: {filename}")

#all_img = soup.find_all('img')
#print(all_img)
# 过滤出油画作品的图片链接
#image_links = []
#for item in soup.find_all('img'):
#    if item.has_attr('src'):
#        image_url = item['src']
#        print(image_url)
    #print(image_url)
#    if 'oil-painting' in item.parent.get('href'):
#        image_url = item['src']
#        image_links.append(image_url)

# 下载图片
#for i, link in enumerate(image_links[:200]):
#    filename = f"oil_painting_{i+1}.jpg"
#    urllib.request.urlretrieve(link, filename)
#    print(f"下载图片 {i+1}: {filename}")
