# -*- coding: utf-8 -*-
from pyspark import SparkConf, SparkContext
"""
AAA
作为标准样例维护，待测试验证
"""

# （1）通过SparkConf和SparkContext连接

#spark集群的地址，如果是本地单机版的，设置为local[x]，x为使用的核数，单机版的即为线程数
spark_host = "spark://spark-master:7077"
app_name = "test"
# 设置连接配置，这里的1g是设置使用的核数
spark_conf = SparkConf().setMaster(spark_host).setAppName(app_name).set("spark.executor.memory", "1g")
spark_context = SparkContext.getOrCreate(conf=spark_conf)
# sparkContext 也可以通过下面的语句转换成sparkSession对象
from pyspark.sql import SparkSession
spark_session = SparkSession(spark_context)

# （2）通过sparkSession连接，
from pyspark.sql import SparkSession
spark_host = "spark://spark-master:7077"
app_name = "test"
spark_session = SparkSession.builder.master(spark_host).appName(app_name).getOrCreate()


hbase_host = ""
table_name = ""
"""
（1）pyspark读取hbase的时候可以根据hbase中record的row_key进行筛选，但是这个筛选是连续的一片式的筛选
（2）hbase的row_key筛选可以通过前缀进行模糊匹配，比如下面的'2019-04-29_'可以取row_key前缀是2019-04-29_的行，设置的stop则是表示以前缀是2019-04-30_的record结束（但是返回结果不包含满足stop前缀的record）
（3）hbase.mapreduce.scan.columns的设置是选取想要读取的hbase中的基本列以{列簇名:列名}的形式表示一列，不同的列之间用空格隔开
"""
conf = {
"hbase.zookeeper.quorum": hbase_host,
"hbase.mapreduce.inputtable": table_name,
"hbase.mapreduce.scan.row.start": '2019-04-29_',
"hbase.mapreduce.scan.row.stop": '2019-04-30_',
"hbase.mapreduce.scan.columns": "family1:column1 family1:column2 family2:column1"

# 其它连接相关conf整理汇总：
# "zookeeper.znode.parent": "/hbase.master",

    }

keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"
# pysaprk连接hbase目前只能通过sparkContext对象，所以这里用的前面设置的spark_context
hbase_rdd = spark_context.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
    "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    "org.apache.hadoop.hbase.client.Result",
    keyConverter=keyConv,
    valueConverter=valueConv,
     conf=conf)

# 如果想通过sparkSesssion对象连接hbase，代码如下
hbase_rdd = spark_session.saprkContext.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
    "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    "org.apache.hadoop.hbase.client.Result",
    keyConverter=keyConv,
    valueConverter=valueConv,
    conf=conf)


""" 
这个函数是一行一行读取hbase_rdd中的record，然后将每个列里面的数据提取出来，最终形成一个dict，这个dict的结构
大概是这样的{column_name1:value1, column_name2:value2, column_name3:value3}，如果hbase里面有些列没有值，就是
压根没存这个字段，可以给这个字段填充一个“Null”值，以便后续可以转为dataframe格式（但是这里的“Null”就是一个字
符串，和dataframe里面本身没有值自动默认为的“Null”是不一样的，前者在用filter这个函数是，条件要写“！=Null”，而后
者则需要用“isNotNull()”这个函数）
"""
import json
def row_transform(row_cells_info, hbase_structure):
    row_cell_info_list = [json.loads(i) for i in row_cells_info]
    row_dict = {}
    hbase_index = 0
    for cell_index in range(len(row_cell_info_list)):
        column_name = row_cell_info_list[cell_index]['qualifier']
        column_value = row_cell_info_list[cell_index]['value']
        if hbase_structure[hbase_index] == column_name:
            row_dict[column_name] = column_value
            hbase_index += 1
        else:
            row_dict[hbase_structure[hbase_index]] = "Null"
            for j in range(hbase_index + 1, len(hbase_structure)):
                if hbase_structure[j] == column_name:
                    row_dict[column_name] = column_value
                    hbase_index = j + 1
                    break
                else:
                    row_dict[hbase_structure[j]] = "Null"
    for j in range(hbase_index, len(hbase_structure)):
        row_dict[hbase_structure[j]] = "Null"
    return row_dict


"""
将HBase RDD转换为DataFrame,这里的hbase_structure对应的是hbase中数据的列名list，如[column_name1,column_name2,column_name3]
并且元素的顺序与hbase中列的顺序对应
"""

def rdd_to_df(hbase_rdd, hbase_structure):
    # 同一个RowKey对应的列之间是用\n分割，进行split，split后每列是个dict
    data_rdd_split = hbase_rdd.map(lambda x: (x[0], x[1].split('\n')))
    # 提取列名和取值
    data_rdd_columns = data_rdd_split.map(lambda x: (x[0], row_transform(x[1], hbase_structure)))
    data = data_rdd_columns.map(lambda x: [x[0]] + [x[1][i] for i in x[1]])
    data_df = sess.createDataFrame(data, ["row_key"] + hbase_structure)
    return data_df

if __name__ == '__main__':
    hbase_rdd = load_from_hbase()  #可以用前面1和2步的代码读取hbase的数据读为rdd
    # 将 rdd格式转换成dataframe格式
    hbase_structure = [column_name1,column_name2,column_name3]
    hbase_df = rdd_to_df(hbase_rdd, hbase_structure)