# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf


def write2hbase():
    spark = SparkSession.builder.appName("nlp").getOrCreate()  # 创建spark对象
    # spark_host = "spark://h01"
    # spark = SparkSession.builder.appName("nlp").master(spark_host).getOrCreate()  # 创建spark对象
    print('spark对象已创建')
    host = 'emr1:2181,emr2:2181,emr3:2181'
    table = 'article_test'

    # 备注：StringToImmutableBytesWritableConverter及StringListToPutConverter是在spark examples模块中的在HBaseConverters.scala中，
    # 在spark1.6存在，2.3.2中已无该类。可使用spark-examples_2.11-1.6.0-typesafe-001.jar
    keyConv = "org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter"
    valueConv = "org.apache.spark.examples.pythonconverters.StringListToPutConverter"
    conf = {"hbase.zookeeper.quorum": host, "hbase.mapred.outputtable": table,
            "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
            "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
            "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable"}

    rawData = ['1,info,article_type,pm', '2,info,article_type,analyze']
    # ( rowkey , [ row key , column family , column name , value ] )
    print('准备写入数据')
    spark.sparkContext.parallelize(rawData)\
        .map(lambda x: (x[0], x.split(',')))\
        .saveAsNewAPIHadoopDataset(conf=conf, keyConverter=keyConv, valueConverter=valueConv)


def hbase_readscan(spark, hbase_host, table):
    """
    :param spark:
    :param hbase_host:
    :param table:
    :return:
        读取hbase 数据Saprk rdd
    """
    conf = {
        "hbase.zookeeper.quorum": hbase_host,
        "hbase.mapreduce.inputtable": table,
        "hbase.mapreduce.scan.row.start": '2019-04-29_',
        "hbase.mapreduce.scan.row.stop": '2019-04-30_',
        "hbase.mapreduce.scan.columns": "family1:column1 family1:column2 family2:column1"
    }

    keyConv ="org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
    valueConv ="org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"
    hbase_rdd = spark.sparkContext.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
                                                   "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                                                   "org.apache.hadoop.hbase.client.Result",
                                                   keyConverter=keyConv,
                                                   valueConverter=valueConv,
                                                   conf=conf,
                                                   batchSize=10000)
    # # 同一个RowKey对应的列之间是用\n分割，进行split，split后每列是个dict
    # print(hbase_rdd.take(50))
    # data_rdd_split = hbase_rdd.map(lambda x:(x[0], x[1].split('\n')))
    hbase_rdd


if __name__ =='__main__':
    write2hbase()



"""
执行：
nohup spark-submit --master yarn --deploy-mode client  --conf "spark.pyspark.driver.python=/usr/bin/python3" --conf "spark.pyspark.python=/usr/bin/python3" /pm/project/cbs-nlp/cbs-nlp-base/main/hbase_test.py
"""