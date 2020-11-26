# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
#import socket
#import multiprocessing
import os
import gevent
import threading
from gevent import socket
from gevent import monkey;monkey.patch_all()

def write_txt_to(length, open_file, set_code, BUFSIZE, clientSocket):
    f=open(open_file,'ab')
    print('length {},txt_to: {}'.format(length, open_file))
    clientSocket.send('OK'.encode(set_code))
    msg=b''
    total=int(length)
    get=0
    while get<total:
        print(clientSocket)
        data=clientSocket.recv(BUFSIZE)
        msg+=data
        get=get+len(data)
    print('总量应收{}，实际接收{}'.format(length,len(msg)))
    if msg:
        print('实际length:{}'.format(len(msg)))
        f.write(msg[:])
        f.close()
        clientSocket.send('txt done'.encode(set_code))

def write_pic_to(length, open_pic_dir, filename, set_code, BUFSIZE, clientSocket):
    pic_save_to=os.path.join(open_pic_dir,filename)
    f=open(pic_save_to,'wb')
    print('length {},pic_to: {}'.format(length, open_pic_dir))
    clientSocket.send('OK'.encode(set_code))
    msg=b''
    total=int(length)
    get=0
    while get<total:
        data=clientSocket.recv(BUFSIZE)
        msg+=data
        get=get+len(data)
    print('总量应收{}，实际接收{}'.format(length,len(msg)))
    if msg:
        print('实际length:{}'.format(len(msg)))
        f.write(msg[:])
        f.close()
        clientSocket.send('pic done'.encode(set_code))

def monitor(pathlist, ADDRlist):
    #TCP/IP4
    ADDRlist['serverSocket']=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #搭建服务
    ADDRlist['serverSocket'].bind(ADDRlist['lADDR'])
    #最大访问量
    ADDRlist['serverSocket'].listen(20)
    print('成功搭建服务器-------正在监听{}端口中'.format(ADDRlist['lADDR']))
    while True:
        ADDRlist['clientSocket'],ADDRlist['rADDR'] = ADDRlist['serverSocket'].accept()
        print('新连接来自{},结构{}'.format(ADDRlist['rADDR'], ADDRlist['clientSocket']))
        msg=ADDRlist['clientSocket'].recv(ADDRlist['txtSIZE'])
        info=msg.decode(ADDRlist['set_code']).split('|')
        if info:
            for i in range(len(info)):
                if info[i]=='None':
                    info[i]=None
            if info[1]=='txt' and info[0]:
                t_txt=threading.Thread(target=write_txt_to, args=(info[0], pathlist['open_filename'],
                    ADDRlist['set_code'],ADDRlist['txtSIZE'],ADDRlist['clientSocket'],))
                t_txt.start()
            elif info[1]=='pic' and info[0] and info[2]:
                t_pic=threading.Thread(target=write_pic_to, args=(info[0], pathlist['open_pic_dir'],
                    info[2], ADDRlist['set_code'], ADDRlist['picSIZE'],ADDRlist['clientSocket'],))
                t_pic.start()
            else:
                print('error >>>',info)
        else:
            print('接收的数据不完整')
        #ADDRlist['clientSocket'].close()
def init_setting():
    pathlist={'open_filename':'', 'pic_name':'', 'open_pic_dir':'', 'dos_filename':'',
            'dos_pic_dir':'', 'dos_config':'', 'open_config': '', 'pic_save_to':''}
    ADDRlist={'lADDR':(), 'rADDR':(), 'rHOST':'', 'rPORT':0, 'picSIZE':0, 'txtSIZE':0,
            'set_code':'', 'lHOST':'', 'lPORT':'', 'clientSocket':'','serverSocket':''}

    print('正在检测配置文件{}'.format('.'*4))
    #--------------发包收包编码和BUFSIZE(缓存大小)--------------------------
    ADDRlist['picSIZE'],ADDRlist['txtSIZE']=8192,1024 #图片为8192,文本为1024
    ADDRlist['set_code']='gbk'
    #-------------建立目录和文件信息-----------------------------
    lhome=os.path.abspath('.')
    lhomelist=lhome.split('\\')
    pathlist['dos_filename']=lhome+'\\MKB\\Monitor_log.txt'
    pathlist['dos_pic_dir']=lhome+'\\MKB\\images\\'
    pathlist['dos_config']=lhome+'\\'+'Monitor_config.txt'
    for n in range(len(lhomelist)):
        pathlist['open_filename']+=lhomelist[n]+'/'
        pathlist['open_pic_dir']+=lhomelist[n]+'/'
        pathlist['open_config']+=lhomelist[n]+'/'
    pathlist['open_filename']+='MKB/Monitor_log.txt'
    pathlist['open_pic_dir']+='MKB/images/'
    pathlist['open_config']+='Monitor_config.txt'
    #-----手动修改Monitor_config.txt文件，如果有配置文件则不需要重复输入IP和端口号
    #----把服务端的配置文件放在客户端同个目录也可，如果配置错误则需要手动删除配置文件。
    if not os.path.exists(pathlist['dos_config']):
        print('未检测出客户端配置文件,请输入新配置信息..........')
        while True:
            if ADDRlist['lHOST'] and ADDRlist['lPORT']:
                break
            if not ADDRlist['lHOST']:
                try:
                    ADDRlist['lHOST']=input('请输入正确的服务器IP地址(如www.xxx.com,xxx.xxx.xxx.xxx):')
                except:
                    print('错误IP格式')
            if not ADDRlist['lPORT']:
                try:
                    ADDRlist['lPORT']=input('请输入正确的服务器端口推荐(6666):')
                except:
                    print('错误端口')
        ADDRlist['lADDR']=(str(ADDRlist['lHOST']),int(ADDRlist['lPORT']))
        f=open(pathlist['open_config'],'w')
        f.write(ADDRlist['lHOST']+'\x0A'+ADDRlist['lPORT'])
        f.close()
        print('已成功生成新客户端配置文件......')
    else:
        f=open(pathlist['open_config'], 'r')
        ff=f.read().split()
        ADDRlist['lHOST'],ADDRlist['lPORT']=ff[0],ff[1]
        ADDRlist['lADDR']=(str(ADDRlist['lHOST']),int(ADDRlist['lPORT']))
        f.close()
        print('已存在客户端配置文件，已成功加载配置信息......')
    print('正在生成配置文件')
    times=0
    while True:
        times+=1
        if os.path.exists(pathlist['dos_filename']) and os.path.exists(pathlist['dos_pic_dir']):
            print('成功生成目录数据变量')
            return pathlist, ADDRlist
        elif times >=5:
            pathlist['open_filename']='D:/MKB/Monitor_log.txt'
            pathlist['open_pic_dir']='D:/MKB/images/'
            pathlist['dos_filename']='D:\\MKB\\Monitor_log.txt'
            pathlist['dos_pic_dir']='D:\\MKB\\images\\'
            print('已经配置默认条件......')
            break
        if not os.path.exists(pathlist['dos_pic_dir']):
            try:
                os.makedirs(pathlist['dos_pic_dir'])
                print('正在生成%s目录' %pathlist['dos_pic_dir'])
            except:
                print('error1>>')
        if not os.path.exists(pathlist['dos_filename']):
            try:
                os.system('type nul >%s' %pathlist['dos_filename'])
                print('正在生成%s文件' %pathlist['dos_filename'])
            except:
                print('error2>>')

def main():
    t_lines=[]
    pathlist, ADDRlist={}, {}
    pathlist, ADDRlist=init_setting()
    t_m=threading.Thread(target=monitor, args=(pathlist,ADDRlist))
    t_m.start()

if __name__=="__main__":
    main()
