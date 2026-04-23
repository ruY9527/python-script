import requests

##  获取 163 上演讲的数据
def one_pdf_get():
    one_url = 'https://video.pollykann.com/api/video/downloadPdf?filmId=20553321a0badeec'
    request_header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-encoding': 'gzip, deflate, br, zstd',
        'Accept-language': 'zh-CN,zh;q=0.9',
        'Cookie': 'JSESSIONID=867BE62D70CB597F8CAC22ED0FA8A03D',
        'Host': 'video.pollykann.com',
        'Referer': 'https://video.pollykann.com/play/20553321a0badeec/1',
        'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    request_header['x-plk-cnonce'] = '0b21ac2ca64446079adf25693f20bf3811356334496'
    request_header['x-plk-signature'] = 'lA1FAQcZPqdH/6jYjchtAND6vmRI/ock4U5y17MmWiA8mokSBxf8E8YQg0Sw7iRU06FS7gncNj1HruFs6glUgw=='
    request_header['x-plk-timestamp'] = '1736560836'
    resp = requests.get(one_url,headers=request_header)
    print(resp.content)
    with open('1.pdf', 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)



if __name__ == '__main__':
    one_pdf_get()