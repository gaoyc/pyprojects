# -*- coding: utf-8 -*-
"""

"""

# url ='http://bbs.tianya.cn/post-house-590038-1.shtml'
import re
import urllib
import urllib.request


url = 'http://bbs.tianya.cn/post-worldlook-1848634-1.shtml'
outRoot = "/tmp"
req = urllib.request.Request(url)
link = urllib.request.urlopen(req)
html = link.read().decode("utf-8")
print(html)
# link = urllib2.urlopen(url)
# html = link.read()
# 获取帖子的基本信息
# 正则表达式，用于提取文章标题
gettitle = re.compile(r'<title>(.*?)</title>')
title = re.findall(gettitle, html)

# 正则表达式匹配HTML中的最大页数的信息。
getmaxlength = re.compile(r'<a href=".*?">(\d*)</a>\s*<a href=".*?"\s*class=.*?>下页</a>')
# 用正则获取最大页数信息
maxlength = getmaxlength.search(html).group(1)
print(maxlength)
# *************************************************************************
# 正则匹配 除所有的帖子内容
gettext = re.compile(r'<div class="bbs-content">\s*([\S\s]*?)\s*</div>')  # [\S\s]匹配任意字符
gettext1 = re.compile(r'<div class="bbs-content clearfix">\s*(.*?)\s*</div>')
getpagemsg = re.compile(r'<div class="atl-info">\s*<span>(.*?)<a href="http:.*uname="(.*)">.*\s*<span>时间：(.*?)</span>')
getnextpagelink = re.compile(r'<a href="(.*?)"\s*class.*?>下页</a>')

# 遍历每一页,获取发帖作者，时间，内容，并打印
filepath = outRoot + '/' + title[0] + '.txt'  # utf-8编码，需要转为gbk .decode('utf-8').encode('gbk')

# filehandle = open(filepath.decode('utf-8').encode('gbk'), 'w')
filehandle = open(filepath.encode('utf-8'), 'w')
# 打印文章标题

filehandle.write(str(title[0].encode('utf-8', 'ignore')) + '\n')

str1 = ""
for pageno in range(1, int(maxlength) + 1):
    i = 0

    filehandle.write('\n\n\n\n\n')
    str1 = '============================' + '第 ' + str(pageno) + ' 页' + '=============================='
    print(str1)
    filehandle.write(str1 + '\n')
    # 获取每条发言的信息头，包含作者，时间
    pagemsg = re.findall(getpagemsg, html)
    if pageno is 1:
        # 获取第一个帖子正文
        text1 = re.findall(gettext1, html)
        # 因为第一条内容由text1获取，text获取剩下的，所以text用i-1索引
    # 获取帖子正文
    text = re.findall(gettext, html)
    for ones in pagemsg:
        if pageno > 1:
            if ones is pagemsg[0]:
                continue  # 若不是第一页，跳过第一个日期

        if 'host' in ones[0]:
            str1 = '楼主：' + ones[1] + '     时间:' + ones[2]
            filehandle.write(str1 + '\n')
        else:
            str1 = ones[0] + ones[1] + '    时间:' + ones[2]
            filehandle.write(str1 + '\n')
        if pageno is 1:  # 第一页特殊处理
            if i is 0:
                str1 = text1[0].replace('<br>', '\n')
                filehandle.write(str1 + '\n')
            else:
                str1 = text[i - 1].replace('<br>', '\n')
                filehandle.write(str1 + '\n')
        else:  # 非第一页的处理
            try:
                str1 = text[i].replace('<br>', '\n')
                filehandle.write(str1 + '\n')
            except IndexError as e:
                print('error occured at >>pageno:' + str(pageno) + '   line:' + str(i))
                print('>>' + text[i - 1])
                print(e)

        i = i + 1
    if pageno < int(maxlength):
        # 获取帖子的下一页链接，读取页面内容
        nextpagelink = 'http://bbs.tianya.cn' + getnextpagelink.search(html).group(1)
        # link = urllib2.urlopen(nextpagelink)
        req = urllib.request.Request(nextpagelink)
        link = urllib.request.urlopen(req)
        html = link.read().decode("utf-8")

filehandle.close()
