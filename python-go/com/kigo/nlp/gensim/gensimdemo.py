from gensim import corpora

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

# texts的每一行代表一篇文档，调用Gensim提供的API建立语料特征（此处即是word）的索引字典，
# 并将文本特征的原始表达转化成词袋模型对应的稀疏向量的表达
texts = [['human', 'interface', 'computer'],
         ['survey', 'user', 'computer', 'system', 'response', 'time'],
         ['eps', 'user', 'interface', 'system'],
         ['system', 'human', 'system', 'eps'],
         ['user', 'response', 'time'],
         ['trees'],
         ['graph', 'trees'],
         ['graph', 'minors', 'trees'],
         ['graph', 'minors', 'survey']]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
print(corpus[0])
# 输出为： [(0, 1), (1, 1), (2, 1)]

# 利用Gensim支持文档的流式处理，进行文件读取方式封装
class MyCorpus(object):
    def iter(self):
        for line in open('mycorpus.txt'):
            yield dictionary.doc2bow(line.lower().split())


# 通过挖掘语料中隐藏的语义结构特征，我们最终可以变换出一个简洁高效的文本向量。
from gensim import models
tfidf = models.TfidfModel(iter) # iter是一个返回bow向量的迭代器

# 将训练好的模型持久化到磁盘上，以便下一次使用：
tfidf.save("./model.tfidf")
## 下一次使用
tfidf = models.TfidfModel.load("./model.tfidf")