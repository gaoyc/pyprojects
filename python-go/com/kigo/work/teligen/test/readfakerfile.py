#!/usr/bin/python3
# encoding :utf-8
import datetime
import os
import threading
import time
import glob

# 读取文件线程
import concurrent.futures
from concurrent.futures import ALL_COMPLETED
from queue import Queue

# 是否动态扫描目录。默认否，只扫描一次。true则一直扫描。
from elasticsearch import Elasticsearch, helpers

isdynamicscan = False
readthd = None

readingflag = ".rding"
readedflag = ".rd"

count = 0
isdone = False

lock = threading.Lock()

def statcount():
    start = datetime.datetime.now()
    print('%s : start the count work' % start)
    while not isdone:
        time.sleep(1)  # 睡眠
        now = datetime.datetime.now()
        elapse = (now - start).seconds
        speed = count / (now - start).seconds
        print('%s bulk total: %s, speed %s , queue size %s' % (
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count, speed, datasqueue.qsize()))

    print('end the count work from %s' % start)

def increateone(add):
    global count
    lock.acquire()
    count += add
    lock.release()

def getfilelist(rootdir, recursive=True):
    # r'D:\tmp\**'
    # for filename in glob.glob(rootdir, recursive=recursive):
    #     print(filename)
    targets = [file for file in glob.glob(rootdir, recursive=recursive) if not file.endswith(readingflag) and not file.endswith(readedflag)]
    return targets


def dealfile(file):
    if os.path.exists(file):
        rding = file + readingflag
        rd = file + readedflag
        os.rename(file, rding)  # 改名, 标识正读取该文件
        thdname = threading.currentThread().name
        print('%s [%s] start to read file %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),thdname, rding))
        with open(rding, mode='r', buffering=1024*1024) as f:
            # line = f.readline()
            for line in f:
                if len(line) == 0:  # 零长度指示 EOF
                    continue
                retstr = parsefakerdata(line)
                # print(retstr)
                datasqueue.put(retstr)

        os.rename(rding, rd)  # 改名, 标识已读取该文件
        print('%s [%s] finish to read file %s' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),thdname, rd))


def startread(dir):
    with concurrent.futures.ThreadPoolExecutor(max_workers=readthd) as executor:  # max_workers如不指定，默认为机器核数
        first = True
        while first:
            # 通过推导方式，future为 {future: file}的字典形式
            futures = {executor.submit(dealfile, file): file for file in getfilelist(dir)}
            # 注意executor.submit为异步执行，所以需要等待全部完成,在重新读取文件
            concurrent.futures.wait(futures, timeout=None, return_when=ALL_COMPLETED)
            first = isdynamicscan


def parsefakerdata(strdata):
    # 15088385092,210727197206212172,注册北京名称有些.任何那么如此单位点击一下
    meta = ['phone', 'ssn', 'msg']
    values = strdata.split(',')
    json = dict(zip(meta, values))
    esreq = {
        '_op_type': 'index',  # bulk支持的操作有 index(默认)，update, create, delete
        '_index': index,
        '_type': '_doc',
        '_source': json
    }
    return esreq


def bulk2es():
    # es = Elasticsearch(hosts=['localhost'], port=9200)
    while True:
        actions = []
        for i in range(bulksize):
            if not datasqueue.empty():  # 不能使用not_empty()，会存在true但实际元素为空的情况
                actions.append(datasqueue.get())
            else:
                break

        actionsize = len(actions)
        if actionsize > 0:
            print(f"action {actions}")
            increateone(actionsize)
            # 使用bulk方式写入es, 注意与streaming_bulk与parallel_bulk类似的区别，调用即执行。
            # helpers.bulk(client=es, actions=actions)



if __name__ == '__main__':

    # path = r'D:\tmp\**'
    path = r'D:\tmp\fakerdata.log2*'
    index = 'idx_faker_test'

    bulksize = 2

    datasqueue = Queue(-1)
    startread(path)

    bulk2es()

    # for file in glob.glob(path):
    #     print(file)
