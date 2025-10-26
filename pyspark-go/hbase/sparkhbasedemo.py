# -*- coding: utf-8 -*-

import os
from pyspark import SparkContext, HiveContext, SparkConf
import pdb

from pyspark import sql

import os

from datetime import datetime

'''
pyspark 读取 hbase
1.function: pyspark - spark-2.3.2 - read data from hbase-1.4.9_stable
'''

print('start time :', datetime.now())

os.environ['PYSPARK_PYTHON']="/Library/Frameworks/Python.framework/Versions/3.6/bin/python3"

#os.environ['PYSPARK_PYTHON']="/Users/lixujian/Documents/software/py3env/bin/python3"

conf = SparkConf()

conf.setMaster("local[*]")

conf.setAppName('zsk app')

conf.set("spark.driver.host", "localhost")

sc = SparkContext(conf = conf)

print ('&'*140)

print ('SparkContext create well done ...')



#host = 'localhost'

#host = '172.16.1.115'

#host = '10.10.126.40'

host = '10.10.2.2,10.10.2.3,10.10.2.4'

port = '2181'

table_name = 'lxj_test'


hbase_conf = {
        "hbase.zookeeper.quorum": host,
        "hbase.zookeeper.property.clientPort": port,
        "hbase.mapreduce.inputtable": table_name,
# "hbase.mapreduce.scan.columns": "cf:age",
# "hbase.mapreduce.scan.columns": "cf:name",
# "hbase.mapreduce.scan.row.start":
# "hbase.mapreduce.scan.row.stop":
# "hbase.mapreduce.scan.column.family":
# "hbase.mapreduce.scan.columns":
# "hbase.mapreduce.scan.timestamp":
# "hbase.mapreduce.scan.timerange.start":
# "hbase.mapreduce.scan.timerange.end":
# "hbase.mapreduce.scan.maxversions":
# "hbase.mapreduce.scan.cacheblocks":
# "hbase.mapreduce.scan.cachedrows":
        "hbase.mapreduce.scan.batchsize": '1000',
    }


keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"

print('*' * 140)

# newAPIHadoopRDD(inputFormatClass, keyClass, valueClass, keyConverter=None, valueConverter=None, conf=None, batchSize=0)

hbase_rdd = sc.newAPIHadoopRDD(

    "org.apache.hadoop.hbase.mapreduce.TableInputFormat",

    "org.apache.hadoop.hbase.io.ImmutableBytesWritable",

    "org.apache.hadoop.hbase.client.Result",

    keyConverter = keyConv,

    valueConverter = valueConv,

    conf = hbase_conf,

    batchSize = 1000,

    )



print (' connection hbase pass ...')

print ('#' * 140)



#count = hbase_rdd.count()

#hbase_rdd.cache()

#print ('count =', count)



output = hbase_rdd.collect()

for k, v in output:

    print ('k :', k)

    print ('v :', v)

    break

print ('End time :', datetime.now())

print ('All is well done ...')

# pyspark 写 hbase

# -*- coding: utf-8 -*-

import os

from datetime import datetime

from pyspark import SparkContext, HiveContext, SparkConf

import pdb

from pyspark import sql

from pyspark.sql import SparkSession

'''

    function: pyspark - spark-2.3.2 - write data to hbase-1.4.9_stable

'''

print ('$'*140)

print ('start time :', datetime.now())

os.environ['PYSPARK_PYTHON']="/Library/Frameworks/Python.framework/Versions/3.6/bin/python3"

conf = SparkConf()

conf.setMaster("local[*]")

conf.setAppName('zsk app')

conf.set("spark.driver.host", "localhost")



sc = SparkContext(conf = conf)

print ('create SparkContext well done ...')



#host = '172.16.1.115'

#host = 'localhost,'

host = '10.10.2.2,10.10.2.3,10.10.2.4'

port = '2181'

table_name = 'lxj_test'



print ('*' * 140)



keyConv = "org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter"

valueConv = "org.apache.spark.examples.pythonconverters.StringListToPutConverter"

hbase_conf={

    "hbase.zookeeper.quorum": host,

    "hbase.zookeeper.property.clientPort": port,

    "hbase.mapred.outputtable": table_name,

    "mapreduce.outputformat.class": "org.apache.hadoop.hbase.mapreduce.TableOutputFormat",

    "mapreduce.job.output.key.class": "org.apache.hadoop.hbase.io.ImmutableBytesWritable",

    "mapreduce.job.output.value.class": "org.apache.hadoop.hbase.client.Result",

# "mapreduce.job.output.value.class": "org.apache.hadoop.io.Writable",

    }

print ('start write data to hbase ...')



# rdd写入的格式为（rowkey, [rowkey,  col_family,  column,  value]）

# ('rowkey002', ['rowkey002, cf, name, eric'])

rawData = ['rowkey013,cf,age,18', 'rowkey014,cf,age,20']

#sc.parallelize(rawData).map(lambda x: (x[0], x.split(','))).saveAsHadoopDataset(

sc.parallelize(rawData).map(lambda x: (x[0:], x.split(','))).saveAsNewAPIHadoopDataset(
        keyConverter = keyConv,
        valueConverter = valueConv,
        conf = hbase_conf,
        )


#pirnt ('start save data as pickle file ...')
#file_name = 'pickle_lixujian'
#sc.parallelize(range(10)).saveAsPickleFile(file_name, 5)

print ('End time :', datetime.now())
print ('All is well done ...')
