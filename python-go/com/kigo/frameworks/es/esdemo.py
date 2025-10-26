# coding=utf-8
from datetime import datetime
from elasticsearch import Elasticsearch

# By default we connect to localhost:9200
# es = Elasticsearch()
# es = Elasticsearch('localhost:9200')
# es = Elasticsearch(hosts=['localhost'], port=9200)
es = Elasticsearch( hosts=[{'host': 'localhost', 'port': 9200}], sniff_on_start=True, maxsize=2)
"""
一些参数是客户端自己添加的，可以在所有的API调用中使用。 Timeout  Ignore
为了与 Python 生态系统兼容，我们使用from_代替 from和doc_type代替type作为参数名称。

python api官方文档：
https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
https://elasticsearch-py.readthedocs.io/en/latest/

"""

# demo-1
# Datetimes will be serialized...
es.index(index="my-index-000001", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
# 响应:
# {'_id': '42', '_index': 'my-index-000001', '_type': 'test-type', '_version': 1, 'ok': True}

# ...but not deserialized
es.get(index="my-index-000001", doc_type="test-type", id=42)['_source']
# 响应:
# {'any': 'data', 'timestamp': '2013-05-12T19:45:31.804229'}

idxName = 'py-test-index'
doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

# demo-2

# 创建索引
res = es.index(index=idxName, doc_type='tweet', id=1, body=doc)
print(res['result'])

# 查询指定ID的文档
res = es.get(index=idxName, doc_type='tweet', id=1)
print(res['_source'])

# 刷写数据
es.indices.refresh(index=idxName)

# 检索-match_all
res = es.search(index=idxName, body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

# 更新文档
doc = {
    'author': 'author_name',
    'text': 'Interesting modified content...',
    'timestamp': datetime.now(),
}
res = es.update(index="test-index", id=1, body=doc)
print(res['result'])


# 删除文档
print(es.delete(index="test-index", id=1))
