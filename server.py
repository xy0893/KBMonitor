from socket import *
import time
import sys
import os

HOST='127.0.0.1'
PORT=6666
BUFIZ=1024
ADDR=(HOST,PORT)

def recvfile(filename):
    print('starting reveive file....')
    f=open(filename, 'wb')
    cliSockfd.send(bytes('no problem', encoding='utf-8'))
    while True:
        data=cliSockfd.recv(4096)
        if data==bytes('EOF', encoding='utf-8'):
            print('recved file success!')
            break
        f.write(data)
    f.close()

def sendfile(filename):
    print('starting send file....')
    cliSockfd.send(bytes('no problem', encoding='utf-8'))
    f=open(filename, 'rb')
    while True:
        data=f.read(4096)
        if not data:
            break
        cliSockfd.send(data)
    f.close()
    time.sleep(1)

def handle1(act, filename):
    if act==bytes('put', encoding='utf-8'):
        print('recving msg!')
        recvfile(filename)
    elif act==bytes('get',encoding='utf-8'):
        print('sending msg!')
        sendfile(filename)
    else:
        print('error!')

def handle2(act):
    if (str(act, ending='utf-8')=='dir'):
        path=sys.path[0]
        every_file=os.listdir(path)
        for filename in every_file:
            cliSockfd.send(bytes(filename+'\t', encoding='utf-8'))
        time.sleep(1)
        eof='EOF'
        cliSockfd.send(bytes(eof, encoding='utf-8'))
        print('all filename has send to client success!')
    else:
        print('command error')

sockfd=socket(AF_INET, SOCK_STREAM)
sockfd.bind(ADDR)
sockfd.listen(5)
while True:
    print('waiting for connection....')
    cliSockfd,addr=sockfd.accept()
    print('...connected from:',addr)
    while True:
        msg=cliSockfd.recv(4096)
        if msg==bytes('close',encoding='utf-8'):
            print('client closed')
            break
        info=msg.split()
        if len(info)==2:
            handle1(info[0],info[1])
        elif len(info)==1:
            handle2(*info)
        else:
            print('command error!')
            break

