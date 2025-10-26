#!/usr/bin/python3
'''
参考：
https://www.runoob.com/python3/python3-date-time.html
'''
import time  # 引入time模块

# 用于获取当前时间戳
ticks = time.time()
print("当前时间戳为:", ticks) # 结果样例，当前时间戳为: 1634472267.4463282

# 获取当前时间
# 从返回浮点数的时间戳方式向时间元组转换，只要将浮点数传递给如localtime之类的函数。
localtime = time.localtime(time.time())
print("本地时间为 :", localtime)
# time.struct_time(tm_year=2021, tm_mon=10, tm_mday=17, tm_hour=20, tm_min=6, tm_sec=19, tm_wday=6, tm_yday=290,
# tm_isdst=0)

# 获取格式化的时间
# 你可以根据需求选取各种格式，但是最简单的获取可读的时间模式的函数是asctime():
localtime = time.asctime( time.localtime(time.time()) )
print("本地时间为 :", localtime)


# 我们可以使用 time 模块的 strftime 方法来格式化日期，：
# time.strftime(format[, t])

# 格式化成2016-03-20 11:45:39形式
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 格式化成Sat Mar 28 22:24:24 2016形式
print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

# 将格式字符串转换为时间戳
a = "Sat Mar 28 22:24:24 2016"
print(time.mktime(time.strptime(a, "%a %b %d %H:%M:%S %Y")))