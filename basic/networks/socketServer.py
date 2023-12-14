#!/usr/bin/python3

import socket
import sys

server_socket = socket.socket(socket.AF_INET, socket.STREAM)

hostname = socket.gethostname()
port = 9988

server_socket.bind((hostname, port))
server_socket.listen(5)

while True:
    client_socket,addr = server_socket.accpet()
    print("连接地址： %s " %(addr))
    msg='欢迎访问菜鸟教程！'+ "\r\n"
    client_socket.send(msg.encode('utf-8'))
    client_socket.close()