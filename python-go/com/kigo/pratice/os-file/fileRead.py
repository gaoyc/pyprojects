# encoding :utf-8
import os

def listdir(path):
    for file in os.listdir(path):
        print(file)



"""
通过glob模块通配过滤
"""
def listdirByGlob():
    import glob
    # 字符串前加r作用是去除转义字符.即如果是“\n”那么表示一个反斜杠字符，一个字母n，而不是表示换行了。
    # 以r开头的字符，常用于正则表达式，对应着re模块。
    # D:\tmp   c:\windows\*.exe

    # 从Python版本3.5开始，glob模块支持该"**"指令（仅当您传递recursive标志时才会解析该指令）：
    # for filename in glob.glob(r'D:\tmp\**', recursive=True):
    for filename in glob.glob(r'D:\tmp\*'):
        print(filename)
    # direction = r'c:\windows'
    # for filename in glob.glob(direction + r'\*.exe'):
    #    其中, r‘’用于保证数据类型不被改变\*用来表示。。。额反正一定要带的

    #



if __name__ == "__main__":
    # listdir("/tmp")
    listdirByGlob()