# coding=utf-8
'''
测试es update性能, 对比新增bulk、 update、update+script的性能差异
'''
import datetime
from elasticsearch import Elasticsearch, helpers
from faker import Faker
from faker.providers import BaseProvider

#################################################
# 配置参数
# 测试条数
doccnt = 10000

# es bulk单批提交
bulksize=1000
idx = 'idx_update_test3'
#################################################

es = Elasticsearch(hosts=['localhost'], port=9200, sniff_on_start=True)
# 创建对象，默认生成的数据为为英文，使用zh_CN指定为中文, 或多语言
fake = Faker('zh_CN')
# fake = Faker(locale=['en_US', 'zh_CN'])  # ['en_US', 'zh_CN']

actions = []
def bulkupdate():
    start = datetime.datetime.now()
    for i in range(doccnt):
        source = {
            "doc": { # update api，soucrce内容需要放在doc结构里面
                "msg": fake.text(),
            },
            "doc_as_upsert": "true" # 如不存在，则插入，不设置默认会报错
        }
        action = {
            '_op_type': 'update',  # bulk支持的操作有 index(默认)，update, create, delete
            '_index': idx,
            '_type': '_doc',
            '_id': i,
            '_source': source
        }
        actions.append(action)

        if len(actions) == bulksize:
            # print(f"action {actions}")
            # 使用bulk方式写入es, 注意与streaming_bulk与parallel_bulk类似的区别，调用即执行。
            helpers.bulk(client=es, actions=actions)
            actions.clear()
            print('total bulk submit: %d' % i)

    # 提交最后一批
    helpers.bulk(client=es, actions=actions)

    now = datetime.datetime.now()
    elapse = (now - start).seconds
    speed = doccnt / (now - start).seconds
    print('finish bulk update, cnt %d, elapse %d sec, speed %d' % (doccnt, elapse, speed))


if __name__ == "__main__":
    bulkupdate()

