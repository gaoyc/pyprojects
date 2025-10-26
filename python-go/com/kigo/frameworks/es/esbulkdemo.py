# coding=utf-8
"""
bulk API可以在单个请求中一次执行多个操作(index,udpate,create,delete)，使用这种方式可以极大的提升索引性能。

在这里我们使用elasticsearch模块的helpers，helpers是bulk的帮助程序，是对bulk的封装。有三种方式bulk（），streaming_bulk（），parallel_bulk（），都需要接受Elasticsearch类的实例和一个可迭代的actions.actions里面的操作可以有多种。

官网：https://elasticsearch-py.readthedocs.io/en/master/helpers.html

版本对应关系，不同的elasticsearch版本要求不同的客户端版本，简单参考：
# Elasticsearch 6.x
elasticsearch>=6.0.0,<7.0.0
# Elasticsearch 5.x
elasticsearch>=5.0.0,<6.0.0
# Elasticsearch 2.x
elasticsearch>=2.0.0,<3.0.0

安装依赖:
pip3 install "ElasticSearch==7.9"
pip3 install faker

"""
import datetime
import random
from collections import deque

from elasticsearch import Elasticsearch, helpers
from faker import Faker

es = Elasticsearch(hosts=['localhost'], port=9200)
# es = AsyncElasticsearch(hosts=['localhost'], port=9200)

# 创建对象，默认生成的数据为为英文，使用zh_CN指定为中文, 或多语言
fake = Faker('zh_CN')


# fake = Faker(locale=['en_US', 'zh_CN'])  # ['en_US', 'zh_CN']

def bulkes6demo():
    levels = ['info', 'debug', 'warn', 'error']
    actions = []

    for i in range(100):
        level = levels[random.randrange(0, len(levels))]
        action = {
            '_op_type': 'index',  # bulk支持的操作有 index(默认)，update, create, delete
            '_index': 'idx_py_bulk_test',
            '_type': 'doc',
            '_source': {'level': level}
        }
        actions.append(action)

    # 使用bulk方式写入es, 注意与streaming_bulk与parallel_bulk类似的区别，调用即执行。
    helpers.bulk(client=es, actions=actions)

    # streaming_bulk与parallel_bulk类似  需要遍历才会运行
    # 都可以设置每个批次的大小，parallel_bulk还可以设置线程数
    # for ok, respone in helpers.streaming_bulk(es, actions):
    #     if not ok:
    #         print(respone)


# async def bulkes7():
def bulkes7():
    """
    使用elasticserach-py-7.x客户端示例。

    参考：
    官网使用示例Bulk update example：
    https://www.elastic.co/guide/en/elasticsearch/reference/7.10/docs-bulk.html#bulk-update

    POST _bulk
    { "update" : {"_id" : "1", "_index" : "index1", "retry_on_conflict" : 3} }
    { "doc" : {"field" : "value"} }
    { "update" : { "_id" : "0", "_index" : "index1", "retry_on_conflict" : 3} }
    { "script" : { "source": "ctx._source.counter += params.param1", "lang" : "painless", "params" : {"param1" : 1}}, "upsert" : {"counter" : 1}}
    { "update" : {"_id" : "2", "_index" : "index1", "retry_on_conflict" : 3} }
    { "doc" : {"field" : "value"}, "doc_as_upsert" : true }
    { "update" : {"_id" : "3", "_index" : "index1", "_source" : true} }
    { "doc" : {"field" : "value"} }
    { "update" : {"_id" : "4", "_index" : "index1"} }
    { "doc" : {"field" : "value"}, "_source": true}

    :return:
    """
    # 创建对象，默认生成的数据为为英文，使用zh_CN指定为中文, 或多语言
    fake = Faker('zh_CN')
    # fake = Faker(locale=['en_US', 'zh_CN'])  # ['en_US', 'zh_CN']
    docs = 10000
    # texts = [(i, fake.text()) for i in range(docs)]

    index = 'idx_bulk_tmp_test'
    bulk_params = {
        # "bulk-size": 100
    }
    t1 = datetime.datetime.now()
    for i in range(docs):
        body = [
            # bulk支持的操作有 index(默认)，update, create, delete
            {'index': {'_index': index,  '_type': '_doc', '_id': i}},
            {'msg': fake.text()}
        ]
        # print(body)
        es.bulk(body=body, index=index, doc_type='_doc', params=bulk_params)

    t2 = datetime.datetime.now()
    elapse = max((t2 - t1).seconds, 1)
    print(f"finish bulk, total {docs}, elapse {elapse} sec, speed {docs/elapse}' ")
    es.close()


def genhelperdata(num, index):
    for i in range(num):
        action = {
            '_op_type': 'index',  # bulk支持的操作有 index(默认)，update, create, delete
            '_index': index,
            '_type': '_doc',
            '_id': i,
            '_source': {
                "msg": fake.text()
            }
        }
        yield action

def bulkhelper():
    docs = 10000
    index = 'idx_bulk_tmp_test'
    bulk_params = {
        # "bulk-size": 100
    }
    actions = []
    for i in range(docs):
        action = {
            '_op_type': 'index',  # bulk支持的操作有 index(默认)，update, create, delete
            '_index': index,
            '_type': '_doc',
            '_id': i,
            '_source': {
                "msg": fake.text()
            }
        }
        actions.append(action)

    t1 = datetime.datetime.now()
    # 方法一:
    # helpers.parallel_bulk(client=es, actions=actions)
    # for success, info in helpers.parallel_bulk(client=es, actions=actions):
    #     if not success:
    #         print('A document failed:', info)

    # 方法二:
    # If you don’t care about the results, you can use deque from collections:
    deque(helpers.parallel_bulk(client=es, actions=actions, queue_size=500), maxlen=0)

    t2 = datetime.datetime.now()
    elapse = max((t2 - t1).seconds, 1)
    print(f"finish bulk, total {docs}, elapse {elapse} sec, speed {docs/elapse}' ")


if __name__ == '__main__':
    # await bulkes7()
    bulkes7()
    # bulkhelper()
    # bulkes6demo()
