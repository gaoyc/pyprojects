
# 安装 
`pip install Faker`

# 基本使用 
```
from faker import Faker
#创建对象，默认生成的数据为为英文，使用zh_CN指定为中文
fake = Faker('zh_CN')
print(fake.name())#随机生成姓名
print(fake.address())#随机生成地址
print(fake.phone_number())#随机生成电话号码
print(fake.pystr())#随机生成字符串
print(fake.email())#随机生成邮箱地址
for i in range(10):
    print(fake.name())#随机生成10个姓名
```

```
输出：
徐博
云南省玉市璧山梧州路p座 523028
13039830591
RPHadhNxNMISoBTbQbQn
yili@taogang.net
张淑英
叶燕
陈琳
王俊
胡秀荣
阮淑英
徐娟
黄冬梅
梁丽华
袁琴
```

# 常用方法 

## 1、地理信息类
```
city_suffix()：市，县
country()：国家
country_code()：国家编码
district()：区
geo_coordinate()：地理坐标
latitude()：地理坐标(纬度)
longitude()：地理坐标(经度)
postcode()：邮编
province()：省份
address()：详细地址
street_address()：街道地址
street_name()：街道名
street_suffix()：街、路
```

## 2、基础信息类
```
ssn()：生成身份证号
bs()：随机公司服务名
company()：随机公司名（长）
company_prefix()：随机公司名（短）
company_suffix()：公司性质，如‘信息有限公司’
fake.credit_card_expire(start='now', end='+10y', date_format='%m/%y')：随机信用卡到期日如'03/30'
credit_card_full()：生成完整信用卡信息
credit_card_number()：信用卡号
credit_card_provider()：信用卡类型
credit_card_security_code()：信用卡安全码
job()：随机职位
first_name_female()：女性名
first_name_male()：男性名
name()：随机生成全名
name_female()：男性全名
name_male()：女性全名
phone_number()：随机生成手机号
phonenumber_prefix()：随机生成手机号段，如139
```
## 3、邮箱信息类
```
ascii_company_email()：随机ASCII公司邮箱名
ascii_email()：随机ASCII邮箱：
company_email()：
email()：
safe_email()：安全邮箱
```

## 4、网络基础信息类
```
domain_name()：生成域名
domain_word()：域词(即，不包含后缀)
ipv4()：随机IP4地址
ipv6()：随机IP6地址
mac_address()：随机MAC地址
tld()：网址域名后缀(.com,.net.cn,等等，不包括.)
uri()：随机URI地址
uri_extension()：网址文件后缀
uri_page()：网址文件（不包含后缀）
uri_path()：网址文件路径（不包含文件名）
url()：随机URL地址
user_name()：随机用户名
image_url()：随机URL地址
```
## 5、浏览器信息类
```
chrome()：随机生成Chrome的浏览器user_agent信息
firefox()：随机生成FireFox的浏览器user_agent信息
internet_explorer()：随机生成IE的浏览器user_agent信息
opera()：随机生成Opera的浏览器user_agent信息
safari()：随机生成Safari的浏览器user_agent信息
linux_platform_token()：随机Linux信息
user_agent()：随机user_agent信息
```

## 6、数字信息
```
numerify()：三位随机数字
random_digit()：0~9随机数
random_digit_not_null()：1~9的随机数
random_int()：随机数字，默认0~9999，可以通过设置min,max来设置
random_number()：随机数字，参数digits设置生成的数字位数
pyfloat()：
left_digits=5 #生成的整数位数, right_digits=2 #生成的小数位数, positive=True #是否只有正数
pyint()：随机Int数字（参考random_int()参数）
pydecimal()：随机Decimal数字（参考pyfloat参数）
```

## 7、文本加密类
```
pystr()：随机字符串
random_element()：随机字母
random_letter()：随机字母
paragraph()：随机生成一个段落
paragraphs()：随机生成多个段落
sentence()：随机生成一句话
sentences()：随机生成多句话，与段落类似
text()：随机生成一篇文章
word()：随机生成词语
words()：随机生成多个词语，用法与段落，句子，类似
binary()：随机生成二进制编码
boolean()：True/False
language_code()：随机生成两位语言编码
locale()：随机生成语言/国际 信息
md5()：随机生成MD5
null_boolean()：NULL/True/False
password()：随机生成密码,可选参数：length：密码长度；special_chars：是否能使用特殊字符；digits：是否包含数字；upper_case：是否包含大写字母；lower_case：是否包含小写字母
sha1()：随机SHA1
sha256()：随机SHA256
uuid4()：随机UUID
```

## 8、时间信息类
```
date()：随机日期
date_between()：随机生成指定范围内日期，参数：start_date，end_date
date_between_dates()：随机生成指定范围内日期，用法同上
date_object()：随机生产从1970-1-1到指定日期的随机日期。
date_time()：随机生成指定时间（1970年1月1日至今）
date_time_ad()：生成公元1年到现在的随机时间
date_time_between()：用法同dates
future_date()：未来日期
future_datetime()：未来时间
month()：随机月份
month_name()：随机月份（英文）
past_date()：随机生成已经过去的日期
past_datetime()：随机生成已经过去的时间
time()：随机24小时时间
timedelta()：随机获取时间差
time_object()：随机24小时时间，time对象
time_series()：随机TimeSeries对象
timezone()：随机时区
unix_time()：随机Unix时间
year()：随机年份

```

# 自定义provider 

```python
from faker import Faker
fake = Faker()

from faker.providers import BaseProvider

# 创建自定义的类
class MyProvider(BaseProvider):
    def fun1(self):
        return 'xxxxxx'

# 调用 add_provider 方法添加一个provider
fake.add_provider(MyProvider)
fake.fun1()
```
更多用法参考官方文档：https://faker.readthedocs.io/en/master/