"""
演示系统命令调用
官方文档:
tutorial => Brief Tour of the Standard Library => 10.1. Operating System Interface
(https://docs.python.org/3/tutorial/stdlib.html#operating-system-interface)

"""


import os
import subprocess


# 方法一: os模块的exec方法簇：

# 方法二： os模块的system调用
# 仅仅在一个子终端运行系统命令，而不能获取命令执行后的返回信息

os.system("pwd && ls -ltrh")

# 方法三： os模块的popen()函数
# popen方法可以得到shell命令的返回值。os.popen(cmd)后，须要再调用read()或者readlines()这两个命令。输出结果。
retListt = os.popen("pwd").readlines() #这个返回值是一个list
print(retListt)

# 方法四: 使用模块 subprocess
'''
使用subprocess模块能够创建新的进程。能够与新建进程的输入/输出/错误管道连通。并能够获得新建进程运行的返回状态。使用subprocess模块的目的是替代os.system()、os.popen*()、commands.*等旧的函数或模块。
'''
retListt = subprocess.call('ls')
print("subprocess.call:" + retListt)
'''
#也可以使用subprocess.Popen
p = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print(line)

'''