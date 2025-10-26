

# ====================================================
# python2库
# ====================================================
"""
rllib2是Python标准库，功能很强大，只是使用起来稍微麻烦一点。
在Python 3中，urllib2不再保留，迁移到了urllib模块中。urllib2中通过ProxyHandler来设置使用代理服务器。
"""

# proxy_handler = urllib2.ProxyHandler({'http': '121.193.143.249:80'})
# opener = urllib2.build_opener(proxy_handler)
# r = opener.open('http://httpbin.org/ip')
# print(r.read())
import urllib

import requests

"""
也可以用install_opener将配置好的opener安装到全局环境中，这样所有的urllib2.urlopen都会自动使用代理。
"""
# urllib2.install_opener(opener)
# r = urllib2.urlopen('http://httpbin.org/ip')
# print(r.read())


# ====================================================
# python3
# ====================================================

# urllib2/urllib 代理设置。
# =======================

proxy_handler = urllib.request.ProxyHandler({'http': 'http://121.193.143.249:80/'})
opener = urllib.request.build_opener(proxy_handler)
r = opener.open('http://httpbin.org/ip')

# requests 代理设置
# =======================
"""
requests是目前最优秀的HTTP库之一，也是我平时构造http请求时使用最多的库。它的API设计非常人性化，
使用起来很容易上手。给requests设置代理很简单，只需要给proxies设置一个形如 
{'http': 'x.x.x.x:8080', 'https': 'x.x.x.x:8080'} 的参数即可。其中http和https相互独立。
"""
requests.get('http://httpbin.org/ip', proxies={'http': '121.193.143.249:80'}).json()

# 可以直接设置session的proxies属性，省去每次请求都要带上proxies参数的麻烦。
s = requests.session()
s.proxies = {'http': '121.193.143.249:80'}
print(s.get('http://httpbin.org/ip').json())


# HTTP_PROXY / HTTPS_PROXY 环境变量
# =======================
# urllib2 和 Requests 库都能识别 HTTP_PROXY 和 HTTPS_PROXY 环境变量，一旦检测到这些
# 环境变量就会自动设置使用代理。这在用HTTP代理进行调试的时候非常有用，因为不用修改代码，可以
# 随意根据环境变量来调整代理服务器的ip地址和端口。*nix中的大部分软件也都支持HTTP_PROXY环境
# 变量识别，比如curl、wget、axel、aria2c等。
"""
$ http_proxy = 121.193
.143
.249: 80
python - c
'import requests; print(requests.get("http://httpbin.org/ip").json())'
{u'origin': u'121.193.143.249'}

$ http_proxy = 121.193
.143
.249: 80
curl
httpbin.org / ip
{
    "origin": "121.193.143.249"
}
"""

# 在IPython交互环境中，可能经常需要临时性地调试HTTP请求，可以简单通过设置:
#  os.environ['http_proxy'] 增加/取消HTTP代理来实现。
"""
In [245]: os.environ['http_proxy'] = '121.193.143.249:80'
In [246]: requests.get("http://httpbin.org/ip").json()
Out[246]: {u'origin': u'121.193.143.249'}
In [249]: os.environ['http_proxy'] = ''
In [250]: requests.get("http://httpbin.org/ip").json()
Out[250]: {u'origin': u'x.x.x.x'}
"""