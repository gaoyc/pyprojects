# -*- coding:utf-8 -*-
from pyspark.sql import SparkSession
"""

"""
url = "jdbc:hive2://81.20.7.56:24002,81.20.7.40:24002,81.20.7.48:24002,81.20.7.32:24002,81.20.7.24:24002/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=sparkthriftserver2x;saslQop=auth-conf;auth=KERBEROS;principal=spark2x/hadoop.scga_jz_hive.hadoop.com@SCGA_JZ_HIVE.HADOOP.COM"
connProperties = { "driver": "org.apache.hive.jdbc.HiveDriver" }

# 创建SparkSession
spark = SparkSession\
        .builder\
        .appName("Spark2x-jdbc-demo") \
        .getOrCreate()

df = spark.read.jdbc(url=url, properties=connProperties, table="tb_evt_caijian_carbon")
#df = spark.read.format("jdbc").option("url", url).option("driver", "org.apache.hive.jdbc.HiveDriver").option("dbtable", "tb_evt_caijian_carbon").load()

df.sql_ctx.sql("select * from tb_evt_caijian_carbon limit 10").show()
df.sql_ctx.sql("show tables").show()
