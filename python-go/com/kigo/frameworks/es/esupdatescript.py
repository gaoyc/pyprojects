# coding=utf-8
import random

from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(hosts=['localhost'], port=9200, sniff_on_start=True)


# ES-6.7测试OK
# 方法1：update + script
# upscript = {
#    "script" : {
#      "source": "ctx._source.counter += params.abc ",
#       "lang": "painless",
#       "params": {
#         "abc": 100
#    }
#
#   }
#   ,
#   "upsert": {
#         "counter": 1
#     }
# }
# es.update(index='idx_update_test', doc_type='_doc', id='1', body=upscript)


# 方法2：bulk + update + script
actions = []
for i in range(3):
    upscript = {
        "script": { # 如存在记录，则执行script操作。可指定参数，无论是否存在，均执行script操作
            "source": "ctx._source.caller = params.caller ; ctx._source.receiver = params.receiver ; ctx._source.msg = params.msg",
            "lang": "painless",
            "params": {
                "caller": i,
                "receiver": i,
                "msg": "hello," +str(i),
            }

        }
        ,
        "upsert": {  # 如不存在记录，则执行upsert操作
            "newcounter": 10
        }
    }
    action = {
        '_op_type': 'update',  # bulk支持的操作有 index(默认)，update, create, delete
        '_index': 'idx_update_test',
        '_type': '_doc',
        '_id': str(i),
        '_source': upscript
    }
    actions.append(action)

# 使用bulk方式写入es, 注意与streaming_bulk与parallel_bulk类似的区别，调用即执行。
helpers.bulk(client=es, actions=actions)

# 方法3(待验证)：put_script
# es.put_script


