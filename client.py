import sys
import time
import socket


HOST='127.0.0.1'
PORT=6666
BUFSIZ=1024
ADDR=(HOST,PORT)

def recvfile(filename):
    f=open(filename),'wb'
    while True:
        msg=cliSockfd.recv(4096)
        if msg==bytes('EOF', encoding='utf-8'):
            print('recv file success!')
            break
        f.write(msg)
    f.close()

def sendfile(filename):
    f=open(filename,'rb')
    while True:
        msg=f.read(4096)
        if not msg:
            break
        cliSockfd.sendall(msg)
    f.close()
    time.sleep(1)
    cliSockfd.sendall(bytes('EOF', encoding='utf-8'))
    print('send file success')

def confirm(cliSockfd, client_command):
    cliSockfd.send(bytes(client_command, encoding='utf-8'))
    msg=cliSockfd.recv(4096)
    if msg==bytes('no problem', encoding='utf-8'):
        return True

def handle1(act,filename):
    if act=='put':
        if confirm(cliSockfd,client_command):
            sendfile(filename)
        else:
            print('server error1!')
    elif act=='get':
        if confirm(cliSockfd, client_command):
            recvfile(filename)
        else:
            print('server error2!')
    else:
        print('command error!')

def handle2(act):
    if act=='dir':
        cliSockfd.send(bytes(act, encoding='utf-8'))
        while True:
            msg=cliSockfd.recv(1024)
            if msg==bytes('EOF', encoding='utf-8'):
                break
            print(msg.decode())
    else:
        print('command error')
try:
    cliSockfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliSockfd.connect(ADDR)
    print('connect to ',ADDR)
    while True:
        client_command=input('>>>')
        if not client_command:
            continue
        msg=client_command.split()
        if len(msg)==2:
            handle1(msg[0],msg[1])
        elif len(msg)==1 and msg!=['close']:
            handle2(*msg)
        elif len(msg)==1 and msg==['close']:
            cliSockfd.send(bytes('close', encoding='utf-8'))
            break
        else:
            print('command error')
except socket.error:
    print('error:',socket.error)
finally:
    cliSockfd.close()

