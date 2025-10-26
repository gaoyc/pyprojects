#!/usr/bin/python3
# encoding :utf-8
import os
import sys
import time, datetime

def readFile(path):
    f = open(path)
    while True:
        line = f.readline()
        # 零长度指示 EOF
        if len(line) == 0:
            break
        # 每行（`line`）的末尾
        # 都已经有了换行符
        # 因为它是从一个文件中进行读取的
        # print(line, end='')
        dicKeyValues = dealHResultRowToDic(line)

        if 'begintime' in dicKeyValues and 'longitude' in dicKeyValues and 'latitude' in dicKeyValues:
            begintime = int(dicKeyValues['begintime'])
            longitude = dicKeyValues['longitude']
            latitude = dicKeyValues['latitude']
            usernum =  dicKeyValues['usernum']
            if len(longitude) > 0 and not longitude.startswith("0"):
                datetime = timestamp2str(begintime)
                print(usernum  +" " +  datetime +" " + longitude +" " + latitude,end="\n")

    # 关闭文件
    f.close()


def dealHResultRowToDic(line):
    # line = "HResult{key=243639332_01_8409014058_70_73259175095, row=[[begintime=1590985941], [event=86], [usernum=13922727185], [homearea=020],[imsi=460002497253173], [imei=35927906420875], [curarea=020], [neid=100.65.254.21], [lai=10034], [ci=231656778], [longitude=113.399025],[latitude=23.121042], [oldlai=9493], [oldci=0], [oldlongitude=0.000000], [oldlatitude=0.000000], [sid=8A5ED484D5040E], [state=0], [idflag=0],[tmsi=9332A7FB], [spcode=1], [guti=866-208-e3c68b26], [userip=0.0.0.0], [periodtime=54], [cgi=460-00-904909-74], [oldcgi=--0-0], [lac23g=10034],[numtype=0], [relatenumtype=0], [areacode=440106], [extra_latitude=0.000000], [extra_longitude=0.000000], [extra_oldlatitude=0.000000],[extra_oldlongitude=0.000000], [uuid=2be5c121-3837-455b-a2d6-b8d52640452c]]"
    dic = {}
    if "row=" in line:
        array = line.split("row=")
        rows = array[1].split(",")

        for item in rows:
            itemPlc = item.replace("[", "").replace("]", "")
            # print(strip, end=' ')
            keyvalue = itemPlc.split("=")
            dic[keyvalue[0].strip()] = keyvalue[1].strip()
    # print(dic)
    return dic


def timestamp2str(timestamp):
    # # 使用time
    # timestamp = 1381419600
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y%m%d%H%M%S", timeArray)
    # print(otherStyleTime)  # 2013--10--10 23:40:00

    # 使用datetime
    # dateArray = datetime.datetime.fromtimestamp(timestamp)
    # otherStyleTime = dateArray.strftime("%Y%m%d%H%M%S")
    return otherStyleTime






if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("usage: "+ sys.argv[0] +" <sourcePath>")
        path = "/mnt/data/COMPANY/HZ/task-任务/3-方案测试类/1-testData/testdata/zyf-sj-0601.log"
    elif len(sys.argv) > 1:
        path = sys.argv[1]

    print(path)
    readFile(path)





