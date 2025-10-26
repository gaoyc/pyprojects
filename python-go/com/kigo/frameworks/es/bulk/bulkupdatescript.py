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
def bulkupdatescript():
    start = datetime.datetime.now()
    for i in range(doccnt):
        source = {
            "script": { # 如存在记录，则执行script操作。可指定参数，无论是否存在，均执行script操作
                # "source": "ctx._source.caller = params.caller ; ctx._source.receiver = params.receiver ; ctx._source.msg = params.msg",
                "source": "ctx._source.msg = params.msg", # 注意，有些资料示例不需要params.前缀，但实测ES6.7版本需要
                "lang": "painless",
                "params": {
                    # "caller": i,
                    # "receiver": i,
                    "msg": fake.text(),
                }

            }
            ,
            "upsert": {  # 如不存在记录，则执行upsert操作
                "newcounter": 10
            }
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
    print('finish bulk update-script, cnt %d, elapse %d sec, speed %d' % (doccnt, elapse, speed))


if __name__ == "__main__":
    bulkupdatescript()


