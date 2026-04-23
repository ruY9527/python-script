#!/usr/bin/python
# coding=utf-8
import os
import os.path
import shutil
import sys
import paramiko
from time import *


# 定义一个类，表示一台远端linux主机
class Linux(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        self.port = 22
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机
    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print('连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                print(self.chan.recv(65535).decode('utf-8'))
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception as e1:
                if self.try_times != 0:
                    print('连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print('重试3次失败，结束程序')
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()

    # 发送要执行的命令
    def send(self, cmd):
        result = ''
        try:
            cmd += '\r'
            # 发送要执行的命令
            self.chan.send(cmd)
            # 回显很长的命令可能执行较久，通过循环分批次取回回显,执行成功返回true,失败返回false
            while True:
                sleep(0.5)
                ret = self.chan.recv(65535)
                ret = ret.decode('utf-8')
                if (len(ret) > 0):
                    result += ret
                else:
                    return result
        except Exception as e:
            # print("Socket receiving data error! | "+str(e))
            return result  # 出现异常返回None

    #   '''
    #   发送文件
    #   @:param upload_files上传文件路径 例如：/tmp/test.py
    #   @:param upload_path 上传到目标路径 例如：/tmp/test_new.py
    #   '''
    def upload_files(self, upload_files, upload_path):
        tran = None
        try:
            tran = paramiko.Transport(sock=(self.ip, self.port))
            tran.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(tran)
            # result=sftp.put(upload_files, upload_path)
            files = os.listdir(upload_files)  # 上传多个文件
            # files = sftp.listdir(remote_dir)  # 下载多个文件
            for f in files:
                print('')
                print('#########################################')
                print('Uploading file:', (upload_path + '/' + f))
                # sftp.get(remote_dir + '/' + f, os.path.join(local_dir, f))  # 下载多个文件
                res = sftp.put(os.path.join(upload_files, f), upload_path + '/' + f)  # 上传多个文件
                print(res)
                print('Upload file success')
                print('')
        except Exception as ex:
            print(ex)
            if (tran != None):
                tran.close()
        finally:
            if (tran != None):
                tran.close()

    def upload_file(self, upload_file, remote_file):
        tran = None
        try:
            tran = paramiko.Transport(sock=(self.ip, self.port))
            tran.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(tran)
            print('#########################################')
            res = sftp.put(upload_file, remote_file)  # 上传文件
            print(res)
            print('Upload file success')
        except Exception as ex:
            print(ex)
            if (tran != None):
                tran.close()
        finally:
            if (tran != None):
                tran.close()

    def down_file(self, server_path, local_path):
        tran = None
        try:
            tran = paramiko.Transport(sock=(self.ip, self.port))
            tran.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(tran)
            # files = sftp.listdir(remote_dir)  # 下载多个文件
            sftp.get(server_path, local_path)
        except Exception as ex:
            print(ex)
            if (tran != None):
                tran.close()
        finally:
            if (tran != None):
                tran.close()


def deploy(env, host, gitdir):
    path = ''
    print('开始上传dist.zip')
    if (env == '217' or env == '214' or env == 'model_dev'):
        res = host.send('rm -rf /bigdata/datahorizon/dh/ui/dist.zip')  # 删除旧目录
        print(res)
        host.upload_file(gitdir + "/dist.zip", "/bigdata/datahorizon/dh/ui/dist.zip")
        path = 'cd /bigdata/datahorizon/dh/ui;'
        print('开始解压dist.zip')
        res = host.send('rm -rf /bigdata/datahorizon/dh/ui/dist')  # 删除旧目录
        print(res)
    if (env == 'prod'):  # 生产环境部署前端
        res = host.send('rm -rf /mydata/soft/dh/ui/dist.zip')  # 删除旧目录
        print(res)
        host.upload_file(gitdir + "/dist.zip", "/mydata/soft/dh/ui/dist.zip")
        path = 'cd /mydata/soft/dh/ui;'
        print('开始解压dist.zip')
        res = host.send('rm -rf /mydata/soft/dh/ui/dist')  # 删除旧目录
        print(res)

    res = host.send(path + ' unzip dist.zip')
    # sleep(20)
    print(res)


def pkg(gitdir, env):
    os.system("cd " + gitdir + "\n  yarn install \n npm run install")
    # 编译，打包，压缩成zip文件
    if (env == 'model_dev'):
        os.system(
            "cd " + gitdir + "\n  npm cache clean --force \n   npm run builddev   \n rm -r dist.zip \n zip -r dist.zip dist/*")
    if (env == '217'):
        os.system(
            "cd " + gitdir + "\n  npm cache clean --force \n   npm run builddev   \n rm -r dist.zip \n zip -r dist.zip dist/*")
    if (env == "214"):
        os.system(
            "cd " + gitdir + "\n  npm cache clean --force \n   npm run buildstage   \n rm -r dist.zip \n zip -r dist.zip dist/*")
    if (env == 'prod'):
        os.system(
            "cd " + gitdir + "\n  npm cache clean --force \n   npm run build   \n rm -r dist.zip \n zip -r dist.zip dist/*")


def updateGit(gitdir):
    # update svn
    # 更新静态资源文件
    os.system("cd  " + gitdir + "\n git restore . \n git pull")


def main():
    env = ''
    if (len(sys.argv) > 1):
        env = sys.argv[1]
    if (env == ''):
        env = '217'

    reload(sys)
    sys.setdefaultencoding("utf-8")

    gitdir = "/datacenter/soft/datahorizon/pkg-dev/dh_platform/dh-ui"

    if (env == "model_dev"):  # 开发环境
        gitdir = "/datacenter/soft/datahorizon/pkg-dev/env_model_dev/dh_platform/dh-ui"
    if (env == "217"):  # 开发环境
        gitdir = "/datacenter/soft/datahorizon/pkg-dev/env_dev/dh_platform/dh-ui"
    if (env == "214"):  # 测试环境
        gitdir = "/datacenter/soft/datahorizon/pkg-dev/env_test/dh_platform/dh-ui"
    if (env == "prod"):  # 生产环境
        gitdir = "/datacenter/soft/datahorizon/pkg-dev/env_prod/dh_platform/dh-ui"
    updateGit(gitdir)

    print('开始打包')
    pkg(gitdir, env)

    print('准备上传dist.zip')
    host = None
    if (env == 'model_dev'):
        host = Linux('172.21.129.217', 'hadoop', 'YD&BigData8')  # 传入Ip，用户名，密码
    if (env == '217'):
        host = Linux('172.21.129.217', 'hadoop', 'YD&BigData8')  # 传入Ip，用户名，密码
    if (env == '214'):
        host = Linux('172.21.129.214', 'hadoop', 'YD&BigData8')  # 传入Ip，用户名，密码
    if (env == 'prod'):  # 生产上传部署
        host = Linux('112.91.138.99', 'yundee', 'ohdfiuE1kg&g2Si')  # 传入Ip，用户名，密码
    host.connect()
    deploy(env, host, gitdir)
    print('=========OK===========')


if __name__ == '__main__':
    main()