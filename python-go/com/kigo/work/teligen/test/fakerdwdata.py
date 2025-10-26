#!/usr/bin/python3
# encoding :utf-8
import datetime
import getopt
import os
import sys
import threading
import time
from queue import Queue

from faker import Faker

########################################
# args可变参数
outfile = r'D:/tmp/fakerdata.log'
# 生产的单个文件大小
filesize = 10000

########################################
# global count
count = 0
isdone = False

lock = threading.Lock()

cnfaker = Faker(locale=['zh_CN'])  # ['en_US', 'zh_CN']
mixfaker = Faker(locale=['en_US', 'zh_CN'])  # ['en_US', 'zh_CN']


def testfakerspeed():
    while True:
        ssn = cnfaker.ssn()
        phone = cnfaker.phone_number()
        cnfaker.numerify()
        # para = mixfaker.paragraph()
        # text = cnfaker.text()
        # sen = cnfaker.sentence()
        # str = cnfaker.pystr()

        increateone(1)


def gen_put_data():
    while True:
        if id_queue.not_full:
            ssn = cnfaker.ssn()
            phone = cnfaker.phone_number()
            para = mixfaker.paragraph()

            # text = faker.text()
            # sen = faker.sentence()
            # str = faker.pystr()

            data = '%s,%s,%s' % (phone, ssn, para)
            # time.sleep(0.1)
            id_queue.put(data)
            # id_queue.put(1)
        else:
            time.sleep(0.1)


def get_data(m):
    while True:
        if id_queue.not_empty:
            data = id_queue.get()
            # print("线程", m, 'data', data)
            increateone(1)
        else:
            time.sleep(0.1)


def increateone(add):
    global count
    lock.acquire()
    count += add
    lock.release()


def statcount():
    start = datetime.datetime.now()
    print('%s : start the count work' % start)
    while not isdone:
        time.sleep(1)  # 睡眠
        now = datetime.datetime.now()
        elapse = (now - start).seconds
        speed = count / (now - start).seconds
        print('%s bulk total: %s, speed %s , queue size %s' % (
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count, speed, id_queue.qsize()))

    print('end the count work from %s' % start)


def write(outputfile, contents):
    with open(outputfile, 'a') as output:
        output.writelines(contents)  # 向文件写入一个序列字符串列表，如果需要换行则要自己加入每行的换行符。
        # for line in contents:
        #     output.write(line)


def writefakerdata(outPath):
    fileindex = 1
    curcnt = 0
    while True:
        buff = []
        out = outPath + '.' + str(fileindex)
        outtmp = out + ".ing"
        while id_queue.not_empty and len(buff) < filesize:
            buff.append(id_queue.get() + "\n")

        sizes = len(buff)
        # print(f'write sizes', sizes)
        if sizes > 0:
            write(outtmp, buff)
            os.rename(outtmp, out)
            print('%s file writed to %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), out))
            increateone(sizes)
            fileindex =  fileindex + 1


def getargs():
    try:
        # 后接:符号，表示该参数必须指定提供
        opts, args = getopt.getopt(sys.argv[1:], '-h-o:-t', ['help', 'out=', 'thread='])
    except getopt.GetoptError:
        print(f'{sys.argv[1]} -o <outfile> -t <threadNum>')
    for opt, value in opts:
        if opt in ('-h', '--help'):
            print(f'{sys.argv[1]} -o <outfile> -t <threadNum>')
            sys.exit()
        if opt in ('-o', '--out'):
            global outfile
            outfile = value


if __name__ == "__main__":

    getargs()
    print(f'outfile={outfile}')
    id_queue = Queue(2000)
    # id_queue = Queue(-1)

    statcount = threading.Thread(target=statcount)
    statcount.start()

    # # th1 = threading.Thread(target=gen_put_data, )
    # # th1.start()
    for iput in range(1):
        threading.Thread(target=gen_put_data, ).start()
    #
    # # threading.Thread(target=get_data, args=(2, )).start()
    # for iget in range(1):
    #     threading.Thread(target=get_data, args=(iget,)).start()

    # testfakerspeed()

    # 开启写线程
    # threading.Thread(target=writefakerdata, args=(outdir,)).start()
    for writethd in range(1):
        # outfile = outfile + '-' + str(writethd)
        threading.Thread(target=writefakerdata, args=(outfile,)).start()
        print('================')
