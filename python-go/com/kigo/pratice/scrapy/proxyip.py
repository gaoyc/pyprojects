import requests
import re
import random
import urllib.request
import urllib.parse
# 代理list
proxies = []
# proxies = {
#   "http": "http://10.10.1.10:3128",
#   "https": "http://10.10.1.10:1080",
# }



# header字典
# headers={"User-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" }
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            # 'Accept-Encoding':'gzip',
           }

# 指定代理地址
requests.get("http://example.org", proxies=proxies)

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