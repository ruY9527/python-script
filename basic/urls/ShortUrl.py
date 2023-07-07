import pyshorteners as psn


# pip install pyshorteners -i https://mirror.baidu.com/pypi/simple/

def generaShortUrl():
    url = 'https://www.baidu.com/'
    shortUrl = psn.Shortener().clckru.short(url)
    print(shortUrl)

if __name__ == '__main__':
    generaShortUrl()