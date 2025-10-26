# encoding=utf8
# spark 2.4.5版本
from pyspark import SparkConf, SparkContext
# from pyspark.context import SparkContext  ## spark 旧版本

sc = SparkContext("local", "WordCount")  # 初始化配置
# file='/mnt/workIng/working/spark-2.2.0-bin-hadoop2.7/README.md'
# file='D:/working/spark-2.2.0-bin-hadoop2.7/README.md'
# file = 'file:///D:/deploy/spark/spark-3.1.2-bin-hadoop3.2/README.md'
file = 'E:\gaoyc\docs&data\spark\spark-2.4.5-bin-hadoop2.7/README.md'
data = sc.textFile(file)  # 自己随便写的一个txt
# sc.wholeTextFiles
counts = data.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
print("============")
# counts.collect()
print(counts.collect())
# counts.saveAsTextFile('count_resul人t') #结果就在count_result这个文件夹里面
sc.stop()