from threading import Thread

import requests
from beaker import session
from bs4 import BeautifulSoup
import re
import os.path

from requests.adapters import HTTPAdapter

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
headers = {'User-Agent': user_agent}


def getListProxies():
    session = requests.session()
    page = session.get("http://www.xicidaili.com/nn", headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')

    proxyList = []
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    for trtag in taglist:
        tdlist = trtag.find_all('td')
        proxy = {'http': tdlist[1].string + ':' + tdlist[2].string,
                 'https': tdlist[1].string + ':' + tdlist[2].string}
        url = "http://ip.chinaz.com/getip.aspx"  # 用来测试IP是否可用的url
        try:
            response = session.get(url, proxies=proxy, timeout=5)
            proxyList.append(proxy)
            if (len(proxyList) == 10):
                break
        except Exception as e:
            continue

    return proxyList

# https://blog.csdn.net/willib/article/details/52374507
class DownloadImgAndWriteToFile(Thread):
    def run(self):
        proxies = getListProxies()
        proxy = proxies[0]  # 第一个最好设置为自己的本地IP，速度会快一些
        print
        proxy
        nameNumber = 0
        ipIndex = 1
        global queue
        while isRun:
            image = queue.get()
            queue.task_done()
            suffixNum = image.rfind('.')
            suffix = image[suffixNum:]
            fileName = filePath + os.sep + str(nameNumber) + suffix
            nameNumber += 1
            try:
                # 设置超时重试次数及超时时间单位秒
                session.mount(image, HTTPAdapter(max_retries=3))
                response = session.get(image, proxies=proxy, timeout=20)
                contents = response.content
                with open(fileName, "wb") as pic:
                    pic.write(contents)

            except requests.exceptions.ConnectionError:
                print
                '连接超时,URL: ', image
                if ipIndex < 10:
                    proxy = proxies[ipIndex]
                    print
                    '新IP:Port', proxy
                    ipIndex += 1
            except IOError:
                print
                'Io error'
        print
        '图片下载完毕'
