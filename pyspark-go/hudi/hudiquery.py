# encoding=utf-8
import time

from pyspark.sql import SparkSession
"""
# 执行测试:
- windows
bin\spark-submit.cmd  --packages org.apache.hudi:hudi-spark3.1.2-bundle_2.12:0.10.1,org.apache.spark:spark-avro_2.12:3.1.2  --conf 'spark.serializer=org.apache.spark.serializer.KryoSerializer'  file:///D:/gaoyc/sources/PycharmProjects/pyspark-go/hudi/hudiquery.py
"""

# ================ 参数配置 ================
tableName = "hudi_trips_cow"
basePath = "file:///D:/tmp/hudi_trips_cow"
# ================ end 参数配置 ================

spark = SparkSession.builder.getOrCreate()

# # 生成测试数据-只需执行一次
# dataGen = spark.sparkContext._jvm.org.apache.hudi.QuickstartUtils.DataGenerator()
# inserts = spark.sparkContext._jvm.org.apache.hudi.QuickstartUtils.convertToStringList(dataGen.generateInserts(10))
# df = spark.read.json(spark.sparkContext.parallelize(inserts, 2))
# hudi_options = { \
#     'hoodie.table.name': tableName, \
#     'hoodie.datasource.write.recordkey.field': 'uuid', \
#     'hoodie.datasource.write.partitionpath.field': 'partitionpath', \
#     'hoodie.datasource.write.table.name': tableName, \
#     'hoodie.datasource.write.operation': 'upsert', \
#     'hoodie.datasource.write.precombine.field': 'ts', \
#     'hoodie.upsert.shuffle.parallelism': 2, \
#     'hoodie.insert.shuffle.parallelism': 2 \
# }
#
# # 保存生成的模拟数据
# df.write.format("hudi").options(**hudi_options).mode("overwrite").save(basePath)


# 查询测试
tripsSnapshotDF = spark.read.format("hudi").load(basePath)
tripsSnapshotDF.createOrReplaceTempView("hudi_trips_snapshot")

sql = "select fare, begin_lon, begin_lat, ts from  hudi_trips_snapshot where fare > 20.0"

start = time.time()

spark.sql(sql).show()
# spark.sql(sql).collect().count()

end = time.time()
elapse = end - start
ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

print("%s: finish query, start %d ,end %d ,elapse %d secs ,sql: %s" % (ftime, start, end, elapse, sql))


