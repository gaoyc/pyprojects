# coding=utf-8
'''
官网文档： https://faker.readthedocs.io/en/stable/
github地址： https://github.com/joke2k/faker
'''

from faker import Faker
from faker.providers import BaseProvider

# 创建对象，默认生成的数据为为英文，使用zh_CN指定为中文, 或多语言
# fake = Faker('zh_CN')
fake = Faker(locale=['en_US', 'zh_CN'])  # ['en_US', 'zh_CN']

for _ in range(1):
    print('name:\t' + fake.name())
    # 'Lucy Cechtelar'

    print('address:\t' + fake.address())
    # '426 Jordy Lodge
    #  Cartwrightshire, SC 88120-6700'
    text = fake.text()
    sen = fake.sentence()
    para = fake.paragraph()
    str = fake.pystr()
    # 社会安全码(身份证号码)
    ssn = fake.ssn()
    phone = fake.phone_number()
    print('len=%s text: %s' % (len(text), text))
    print('len=%s sen: %s' % (len(sen), sen))
    print('len=%s para: %s' % (len(para), para))
    print('len=%s str: %s' % (len(str), str))
    print('len=%s phone: %s' % (len(phone), phone))

    print('随机URI地址-uri(): ' + fake.uri())
    print('网址文件后缀-uri(): ' + fake.uri_extension())
    print('网址文件（不包含后缀）-uri(): ' + fake.uri_page())
    print('网址文件路径（不包含文件名）-uri(): ' + fake.uri_path())
    print('随机URL地址-uri(): ' + fake.url())


# 自定义provider。创建自定义的类
class MyProvider(BaseProvider):
    def fun1(self):
        return 'xxxxxx'


# 调用 add_provider 方法添加一个provider
# fake.add_provider(MyProvider)
# fake.fun1()


# fake.country() # 国家
# fake.city() # 城市
# fake.city_suffix() # 城市的后缀,中文是：市或县'市'
# fake.name() # 姓名
# fake.last_name() # 姓
# fake.ean8() # 8位条码
# fake.ean13() # 13位条码

# pystr()：随机字符串
# paragraph()：随机生成一个段落
# paragraphs()：随机生成多个段落
# sentence()：随机生成一句话
# sentences()：随机生成多句话，与段落类似
# text()：随机生成一篇文章
# word()：随机生成词语
# words()：随机生成多个词语，用法与段落，句子，类似
