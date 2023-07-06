#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

import paramiko


def initSsh():
    ssh=paramiko.SSHClient()
    ssh.connect(hostname='172.21.129.210',username='1',password='1')
    stdin,stdout,stderr=ssh.exec_command('ifconfig',timeout=10)
    stdout,stderr=stdout.read(),stderr.read()
    res=stdout if stdout else stderr
    print(res.decode())
    ssh.close()#关闭连接


if __name__ == '__main__':
    initSsh()
