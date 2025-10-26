import sys
import time

f = None
try:
    f = open("poem.txt")
    # 我们常用的文件阅读风格
    while True:
        line = f.readline()
        if len(line) == 0:
            break
    print(line, end='') # end='' 会不产生换行
    sys.stdout.flush()  # 立即打印到屏幕
    print("Press ctrl+c now")
    # 为了确保它能运行一段时间
    time.sleep(2)
except IOError:
    print("Could not find file poem.txt")
except KeyboardInterrupt:
    print("!! You cancelled the reading from the file.")

# 在程序退出之前，finally子句得到执行，文件对象总会被关闭。
finally:
    if f:
        f.close()
    print("(Cleaning up: Closed the file)")
