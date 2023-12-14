import socket as f


def getIpBySocket():
    hosts = f.gethostname()
    laptop = f.gethostbyname(hosts)
    print("ip地址是: " + laptop)

if __name__ == '__main__':
    getIpBySocket()