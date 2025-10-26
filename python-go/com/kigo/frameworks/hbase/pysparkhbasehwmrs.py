# _*_ coding: utf-8 _*_
"""
https://support.huaweicloud.com/devg-dli/dli_09_0078.html#section1
使用Spark作业跨源访问数据源-对接HBase-pyspark样例代码
"""
from __future__ import print_function
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, BooleanType, ShortType, LongType, \
    FloatType, DoubleType
from pyspark.sql import SparkSession

if __name__ == "__main__":
    # Create a SparkSession session.
    sparkSession = SparkSession.builder.appName("datasource-hbase").getOrCreate()

    # Createa data table for DLI-associated ct
    # 如果对接的HBase集群未开启Kerberos认证，样例代码参考如下。
    sparkSession.sql(
        "CREATE TABLE testhbase(id STRING, location STRING, city STRING) using hbase OPTIONS (\
        'ZKHost' = '192.168.0.189:2181',\
        'TableName' = 'hbtest',\
        'RowKey' = 'id:5',\
        'Cols' = 'location:info.location,city:detail.city')")

    # 如果对接的HBase集群开启了Kerberos认证，样例代码参考如下。
    # sparkSession.sql(
    #     "CREATE TABLE testhbase(id STRING, location STRING, city STRING) using hbase OPTIONS (\
    #     'ZKHost' = '192.168.0.189:2181',\
    #     'TableName' = 'hbtest',\
    #     'RowKey' = 'id:5',\
    #     'Cols' = 'location:info.location,city:detail.city',\
    #     'krb5conf' = './krb5.conf',\
    #     'keytab'='./user.keytab',\
    #     'principal' ='krbtest')")

    # Create a DataFrame and initialize the DataFrame data.
    dataList = sparkSession.sparkContext.parallelize([("11111", "aaa", "aaa", False, 4, 3, 23, 2.3, 2.34)])

    # Setting schema
    schema = StructType([StructField("id", StringType()),
                         StructField("location", StringType()),
                         StructField("city", StringType()),
                         StructField("booleanf", BooleanType()),
                         StructField("shortf", ShortType()),
                         StructField("intf", IntegerType()),
                         StructField("longf", LongType()),
                         StructField("floatf", FloatType()),
                         StructField("doublef", DoubleType())])

    # Create a DataFrame from RDD and schema
    dataFrame = sparkSession.createDataFrame(dataList, schema)

    # Write data to the cloudtable-hbase
    dataFrame.write.insertInto("test_hbase")

    # Set cross-source connection parameters
    TableName = "table_DupRowkey1"
    RowKey = "id:5,location:6,city:7"
    Cols = "booleanf:CF1.booleanf,shortf:CF1.shortf,intf:CF1.intf,longf:CF1.longf,floatf:CF1.floatf,doublef:CF1.doublef"
    ZKHost = "cloudtable-cf82-zk3-pa6HnHpf.cloudtable.com:2181,cloudtable-cf82-zk2-weBkIrjI.cloudtable.com:2181,cloudtable-cf82-zk1-WY09px9l.cloudtable.com:2181"

# Read data on CloudTable-HBase
jdbcDF = sparkSession.read.schema(schema) \
    .format("hbase") \
    .option("ZKHost", ZKHost) \
    .option("TableName", TableName) \
    .option("RowKey", RowKey) \
    .option("Cols", Cols) \
    .load()
jdbcDF.filter("id = '12333' or id='11111'").show()

# close session
sparkSession.stop()
