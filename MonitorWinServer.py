from socket import *
import time
import os
import sys
#import threading

def get_local_time():
    #返回当前时间函数,导用了time库
    return time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime(time.time()))

def check_clean(dos_filename, dos_pic_dir):
    lines=0
    pic_lists =os.listdir(dos_pic_dir)
    for _ in open(dos_filename):
        lines+=1
    #修改最大存储本文行数
    if lines>=2000:
        os.system('type nul >%s' %dos_filename)
        print('清空文本记录')
    #修改最大图片量
    if len(pic_lists) >1000:
        for pl in pic_lists:
            fpath=dos_pic_dir+pl
            print('正在移除{}{}'.format(fpath,'\x0D'), end='')
            time.sleep(0.001)
            if os.path.isfile(fpath):
                os.remove(fpath)
        print('\x0A成功清空截屏')

def handle(clientSockfd, filetype, file_msg, pic_, set_encoding, BUFSIZE):
    #----握手函数用于排查客户端发送的是图片还是文本数据。
    if filetype==bytes('txt',encoding=set_encoding):
        print('成功握手{}'.format(filetype))
        recvfile(clientSockfd, file_msg, 'txt', set_encoding, BUFSIZE)
    elif filetype==bytes('pic',encoding=set_encoding):
        pic_msg=pic_+'mouse_%s.jpg' %get_local_time()
        print('成功握手{}'.format(filetype))
        recvfile(clientSockfd, pic_msg, 'pic', set_encoding, BUFSIZE)
    else:
        print('握手失败')

def recvfile(clientSockfd, open_msg, filetype, set_encoding, BUFSIZE):
    #----接收数据并且存储本地函数
    print('开始存储数据{}'.format(open_msg))
    #当系统执行到这一条，说明握手函数成功识别了数据类型，则发送NO PROBLEM给
    #客户端，这时客户端依旧在监听，当收到了NO PROBLEM则会发送全部数据包。
    clientSockfd.send(bytes('NO PROBLEM', encoding=set_encoding))
    if filetype=='pic':
        f=open(open_msg,'wb')
    elif filetype=='txt':
        f=open(open_msg,'ab')
    else:
        return False
    while True:
        #开始接收数据并存储到本地
        data=clientSockfd.recv(BUFSIZE)
        if data==bytes('EOF',encoding=set_encoding):
            print('成功存储数据')
            clientSockfd.sendall(bytes('That everything alright',encoding=set_encoding))
            break
        f.write(data)
    f.close()

def main():
    print('正在检测配置文件{}'.format('.'*4))
    current_path=os.path.abspath('.')
    config_name='Monitor_config.txt'
    config_file=current_path+'\\'+config_name
    #-----如果不想弹窗配置客户端，则把服务端配置文件放在客户端同一目录下即可
    if not os.path.exists(config_file):
        HOST,PORT='',0
        while True:
            if HOST and PORT:
                break
            if not HOST:
                try:
                    HOST=input('请输入正确的服务器IP地址推荐(xxx.com,xxx.xxxx.xxx.xxx):')
                except:
                    print('错误IP格式')
            if not PORT:
                try:
                    PORT=input('请输入正确的服务器端口推荐(6666):')
                except:
                    print('错误端口')
        lADDR=(HOST,int(PORT))
        f=open(config_file,'w')
        f.write(HOST+'\x0A'+PORT)
        f.close()
    else:
        f=open(config_file, 'r')
        ff=f.read().split()
        HOST,PORT=ff[0],ff[1]
        lADDR=(HOST,int(PORT))

    BUFSIZE=1024
    set_encoding='utf-8'
    msg_to='D:/Monitor/Monitor.txt'
    pic_='D:/Monitor/image/'
    dos_pic_dir='D:\\Monitor\\image\\'
    dos_filename='D:\\Monitor\\Monitor.txt'

    times=0
    print('正在布置环境{}'.format('.'*8))
    #上面都是基础变量

    while True:
        #进入第一段创建环境的循环
        times+=1
        if os.path.exists(dos_pic_dir) and os.path.exists(dos_filename):
            print('成功创建{}和{}'.format(dos_pic_dir,dos_filename))
            break
        elif times>=5:
            print('无法成功创建{}和{}'.format(dos_pic_dir,dos_filename))
            print('请手动创建，或管理权限执行。')
            sys.exit()
        if not os.path.exists(dos_pic_dir):
            os.system('mkdir %s' %dos_pic_dir)
        if not os.path.exists(dos_filename):
            os.system('type nul >%s' %dos_filename)
    check_clean(dos_filename, dos_pic_dir)

    #创建数字通信类型，这里用的是IP4,TCP
    serverSockfd=socket(AF_INET, SOCK_STREAM)
    #搭建服务器,如果无法连接则用默认使用本机IP和6666端口搭建
    try:
        serverSockfd.bind(lADDR)
    except:
        HOST='127.0.0.1'
        PORT=6666
        lADDR=(HOST,PORT)
        serverSockfd.bind(lADDR)
    #监听IP最大上限，也就是能有多少台客户端可以访问。
    serverSockfd.listen(10)

    while True:
        #核心监听循环
        print('监听{}端口中{}'.format(PORT,'.'*6))
        #把监听到的客户端和IP 存入clientsockfd和rADDR变量
        clientSockfd,rADDR=serverSockfd.accept()
        print('...连接来自:',rADDR)
        while True:
            msg=clientSockfd.recv(BUFSIZE)
            #split()可以理解成将字符串转换成数组，如'ab a c 55'>>>['ab', 'a', 'c', '55']
            info=msg.split()
            #---------threading.Thread 多线程模块导入会有BUG，尚未解决暂时放着。
            #t_reading=threading.Thread(target=handle,args=(clientSockfd,
            #    info[0], msg_to, pic_, set_encoding, BUFSIZE))
            #t_reading.start()
            handle(clientSockfd, info[0], msg_to, pic_, set_encoding, BUFSIZE)
    return True
if __name__ == "__main__":
    main()
