# encoding: utf-8
""""
![快宝平台-地址库服务-地址清洗](https://open.kuaidihelp.com/api/1019) <https://open.kuaidihelp.com/api/1019>
"""
import http.client , urllib, hashlib
import time

conn = http.client.HTTPSConnection("kop.kuaidihelp.com")

appId = '''50001'''
method = '''cloud.address.cleanse''';
ts = int(time.time());
appKey = '''bdf3b5f50865ac813cbdfd6c9b572b79'''

# 计算签名
signStr = appId + method + str(ts) + appKey;
sign = hashlib.md5(signStr.encode('utf8')).hexdigest()

payload_list={}
payload_list['app_id']=appId
payload_list['method']=method
payload_list['ts']=str(ts)
payload_list['sign']=sign
payload_list['data']='''{
    "multimode":true,
    "address":" 广东省梅州市五华县安流镇青江村琴江御城201商场\r深圳市龙华新区观澜街道库坑新围村皇帝印工业区D栋\r杭州市中河中路258号瑞丰国际商务大厦5F",
    "cleanTown":true
}'''

payload =urllib.parse.urlencode(payload_list)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    }

conn.request("POST", "/api", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))