# -*- coding: utf-8 -*-
"""
图片爬虫示例
https://www.toutiao.com/a6572875013999821316/?tt_from=android_share&utm_campaign=client_share&timestamp=1530408599&app=news_article&iid=36521543118&utm_medium=toutiao_android
"""
import re
import random
import urllib.request
import urllib.parse
import os
from bs4 import BeautifulSoup

# 代理list
proxies = []

# header字典
# headers={"User-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" }
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            # 'Accept-Encoding':'gzip',
           }


def get_proxy():
    # 西刺免费代理IP
    url = "http://www.xicidaili.com"
    req = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    IP = re.compile('<td>(\d+)\.(\d+)\.(\d+)\.(\d+)</td>\s*<td>(\d+)</td>')
    proxy_ip = IP.findall(html)
    for each in proxy_ip:
        proxies.append(":".join([(".".join(each[0:4])), each[4]]))
    print(proxies)
    return proxies


def change_proxy():
    proxy = random.choice(proxies)
    if proxy == None:
        proxy_support = urllib.request.ProxyHandler({})
    else:
        proxy_support = urllib.request.ProxyHandler({"http": proxy})

    opener = urllib.request.build_opener(proxy_support)
    # opener.addheaders[("User-agent", headers["User-agent"])]
    urllib.request.install_opener(opener)
    print('智能切换代理: %s' %('本机' if proxy == None else proxy))


def url_open(url):

    # req = urllib.request.Request(url)
    # req.add_header("User-Agent","Mozilla/5.0 (Window NT 6.1; WOW64) "
    #                            "AppleWbKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    return html


def get_pagenum(url):  # 获取jandan网站的页面号
    html = url_open(url).decode("utf-8")
    print("get_pagenum, get html=%s", html)
    num_re = re.compile(r'<span class="current-comment-page">\[d{4}\]</span>')
    num = num_re.search(html)
    a = re.compile(r'\d{4}')
    num_b = a.search(num.group())
    return num_b.group()


def get_images(url):
    html = url_open(url).decode("utf-8")
    img_list = []
    jpg_re = re.compile(r'<img src="//([^"]+\.jpg)">')
    # 当给出的正表达中带有一个括号时, 列表的元素为字符串
    # 此时子服从的内容与括号中的正则表达式相对应(不是整个正则表达式的匹配内容)
    imgurl = jpg_re.findall(html)
    for each in imgurl:
        img_list.append(each)

    # print(img_list)
    return img_list


def save_imgs(img_list):
    i = 0
    for each in img_list:
        i+=1
        filename = each.split("/")[-1]
        with open(filename, "wb") as f:
            img = url_open("http://%s" %each)
            f.write(img)
            print("下载本页的第%s张图片, 名称为%s" %(i, filename))


def download_mm(dir, url):
    if not os.path.isdir(dir):
        os.mkdir(dir)
        os.chdir(dir)
    else:
        os.chdir(dir)

    url = url
    print("准备下载图片到目录%s, url=%s" % (dir, url))
    page_num = int(get_pagenum(url))
    for i in range(20):
        page_num -= 1
        pageurl = url + "page-" + str(page_num) + "#comments"
        print("下载第%s页图片, url=%s" % (page_num, pageurl))
        imgurl = get_images(pageurl)
        saveimg = save_imgs(imgurl)


if __name__=="__main__":
    dir = "/tmp/PaPa"
    url = "http://jandan.net/ooxx/"
    print(headers['User-Agent'])
    get_proxy()
    change_proxy()
    download_mm(dir, url)