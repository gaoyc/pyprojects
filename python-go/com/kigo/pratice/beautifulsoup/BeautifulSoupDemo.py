#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import Tag
import requests  ##导入requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Accept-Encoding': 'gzip',
}
URL_1024 = "http://x3.1024lualu.click/pw/thread.php?fid=22"
start_html = requests.get(URL_1024, headers=headers)
start_html.encoding = 'utf-8'
bsObj = BeautifulSoup(start_html.text, 'html.parser')


def getHtml(url):
    page = requests.get(url)
    html = page.text
    return html

# Python爬虫实战(二):爬取天涯帖子(只看楼主)
def getText(html):
    get_text = Tag.get_text
    soup = BeautifulSoup(html, 'html.parser')

    author_info = soup.find_all('div', class_='atl-info')
    listauthor = [x.get_text() for x in author_info]

    list_info = soup.find_all('div', class_='bbs-content')
    listtext = [x.get_text() for x in list_info]

    global i
    if i > 1:
        listtext = [""] + listtext

    for x in range(len(listauthor)):
        if "楼主" in listauthor[x]:
            print(listtext[x].strip())


if __name__ == '__main__':
    for i in range(1, 6):
        url = ("http://bbs.tianya.cn/post-feeling-4286798-%s.shtml" % str(i))
        html = getHtml(url)
        getText(html)

