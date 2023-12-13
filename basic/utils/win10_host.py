#coding=utf-8
import socket
from python_hosts import Hosts, HostsEntry

host_path = 'C:\Windows\System32\drivers\etc\hosts'

def getPingIp():
    host_name = 'thisforyou.cn'
    ip = socket.gethostbyname(host_name)
    print(ip)
    return ip

def readHostFile():
    # 获取ip
    ip = getPingIp()
    hosts = Hosts()
    hosts.remove_all_matching(name='thinkmall-mysql')
    hosts.remove_all_matching(name='thinkmall-nacos')
    hosts.remove_all_matching(name='thinkmall-redis')
    hosts.write()

    ## 写入新的host
    new_entry_mysql = HostsEntry(entry_type='ipv4', address=ip, names=['thinkmall-mysql'])
    new_entry_nacos = HostsEntry(entry_type='ipv4', address=ip, names=['thinkmall-nacos'])
    new_entry_redis = HostsEntry(entry_type='ipv4', address=ip, names=['thinkmall-redis'])
    hosts.add([new_entry_mysql, new_entry_nacos,new_entry_redis])
    hosts.write()
    print(hosts)

# 将域名的地址修改到hosts中;如果你不愿每次手动获取ip将其映射上去
if __name__ == '__main__':
    readHostFile()