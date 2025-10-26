# coding=utf-8
"""
测试es update性能, 对比新增bulk、 update、update+script的性能差异
"""
import datetime
from elasticsearch import Elasticsearch, helpers
from faker import Faker
from faker.providers import BaseProvider

#################################################
# 配置参数
# 测试条数
doccnt = 30000

# es bulk单批提交
bulksize=1000
idx = 'idx_update_test'
#################################################

es = Elasticsearch(hosts=['localhost'], port=9200, sniff_on_start=True)
# 创建对象，默认生成的数据为为英文，使用zh_CN指定为中文, 或多语言
fake = Faker('zh_CN')
# fake = Faker(locale=['en_US', 'zh_CN'])  # ['en_US', 'zh_CN']


def genaction(esid, actiontype, line):
    """
    构造es bulk的action
    :param esid:
    :param actiontype: 支持index、update、update-script
    :param line: 内容
    :return:
    """
    action = {}
    if actiontype == 'index':
        source = {
            "msg": line,
        }
        action = {
            '_op_type': 'index',  # bulk支持的操作有 index(默认)，update, create, delete
            '_index': idx,
            '_type': '_doc',
            '_id': esid,
                '_source': source
        }
    elif actiontype == 'update':
        source = {
            "doc": { # update api，soucrce内容需要放在doc结构里面
                "msg-up": line,
            },
            "doc_as_upsert": 'true'  # 如不存在，则插入，不设置默认会报错
        }
        action = {
            '_op_type': 'update',  # bulk支持的操作有 index(默认)，update, create, delete
            '_index': idx,
            '_type': '_doc',
            '_id': esid,
            '_source': source
        }
    elif actiontype == 'update-script':
        source = {
            "script": {  # 如存在记录，则执行script操作。可指定参数，无论是否存在，均执行script操作
                "source": "ctx._source.msgupspt = params.msgupspt",  # 注意，有些资料示例不需要params.前缀，但实测ES6.7版本需要
                "lang": "painless",
                "params": {
                    "msgupspt": line
                }

            }
            ,
            "upsert": {  # 如不存在记录，则执行upsert操作
                "msgupspt": line
            }
        }
        action = {
            '_op_type': 'update',  # bulk支持的操作有 index(默认)，update, create, delete
            '_index': idx,
            '_type': '_doc',
            '_id': esid,
            '_source': source
        }
    return action


def bulk2es(actionsqueue):
    """
    bulk datas to es
    :param actionsqueue: action数据列表
    :return:
    """
    i = 0
    onebulks = []
    actioncnt = len(actionsqueue)
    start = datetime.datetime.now()
    for it in actionsqueue:
        onebulks.append(it)
        if len(onebulks) == bulksize:
            # print(f"action {actions}")
            # 使用bulk方式写入es, 注意与streaming_bulk与parallel_bulk类似的区别，调用即执行。
            helpers.bulk(client=es, actions=onebulks)
            onebulks.clear()
            i += bulksize
            print('total bulk submit: %d' % i)

    # 提交最后一批
    helpers.bulk(client=es, actions=onebulks)
    now = datetime.datetime.now()
    elapse = (now - start).seconds
    if elapse == 0: elapse = 1
    speed = doccnt / elapse
    print('finish bulk2es, cnt %d, elapse %d sec, speed %d' % (actioncnt, elapse, speed))


def startbulktest():
    start = datetime.datetime.now()
    texts = [(i, fake.text()) for i in range(doccnt)]
    indexs = [genaction(i, 'index', msg) for i, msg in texts]
    updates=[genaction(i, 'update', msg) for i, msg in texts]
    updatescripts=[genaction(i, 'update-script', msg) for i, msg in texts]
    now = datetime.datetime.now()
    print('data prepared, elapse %d sec' % (now-start).seconds)
    t1= datetime.datetime.now()
    bulk2es(updates)
    t2 = datetime.datetime.now()
    bulk2es(updatescripts)
    t3 = datetime.datetime.now()
    bulk2es(indexs)
    t4 = datetime.datetime.now()
    print('finish bulk test, total count %d, index elapse %d sec, update  elapse %d sec, update-script elapse %d sec.'
          % (doccnt, (t2-t1).seconds, (t3-t2).seconds, (t4-t3).seconds))


if __name__ == "__main__":
    startbulktest()


# 测试结果
# index-新增
# finish bulk2es, cnt 30000, elapse 59 sec, speed 508

# update-更新
# finish bulk2es, cnt 30000, elapse 74 sec, speed 405

# update-script-更新
# finish bulk2es, cnt 30000, elapse 91 sec, speed 329


# ES入库-更新结果数据样例：
# {
#   "_index" : "idx_update_test",
#   "_type" : "_doc",
#   "_id" : "1",
#   "_version" : 6,
#   "_seq_no" : 37993,
#   "_primary_term" : 1,
#   "found" : true,
#   "_source" : {
#     "msg" : """
# 上海上海日期更新组织.这是来源单位行业应该人民完成.
# 地方当然有关一样标题方式.专业学校企业非常.
# 任何提供关于.可以他的主题国际报告开发发布.部分简介来源.对于经济处理系列能够最新.
# 质量网络新闻提供包括经营.处理手机内容人员我的名称研究.
# 女人增加因此学校在线.
# 日期显示这么中文这种程序没有.生产单位网络这是网站所有一定.
# 地址今天登录深圳可以.加入相关等级作者.投资有些也是可能.
# """,
#     "msg-up" : """
# 上海上海日期更新组织.这是来源单位行业应该人民完成.
# 地方当然有关一样标题方式.专业学校企业非常.
# 任何提供关于.可以他的主题国际报告开发发布.部分简介来源.对于经济处理系列能够最新.
# 质量网络新闻提供包括经营.处理手机内容人员我的名称研究.
# 女人增加因此学校在线.
# 日期显示这么中文这种程序没有.生产单位网络这是网站所有一定.
# 地址今天登录深圳可以.加入相关等级作者.投资有些也是可能.
# """,
#     "msgupspt" : """
# 上海上海日期更新组织.这是来源单位行业应该人民完成.
# 地方当然有关一样标题方式.专业学校企业非常.
# 任何提供关于.可以他的主题国际报告开发发布.部分简介来源.对于经济处理系列能够最新.
# 质量网络新闻提供包括经营.处理手机内容人员我的名称研究.
# 女人增加因此学校在线.
# 日期显示这么中文这种程序没有.生产单位网络这是网站所有一定.
# 地址今天登录深圳可以.加入相关等级作者.投资有些也是可能.
# """
#   }
# }