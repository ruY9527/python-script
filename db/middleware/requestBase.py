import requests



def requestBaidu():
    r = requests.get('https://www.baidu.com')
    print(r.status_code)


if __name__ == '__main__':
    requestBaidu()