# encoding=utf-8
from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL Hive integration example") \
    .enableHiveSupport() \
    .getOrCreate()
    # .config("spark.sql.warehouse.dir", warehouse_location)

# 注意集成hive必须指定`.enableHiveSupport()`, 参考说明: https://spark.apache.org/docs/3.2.1/sql-data-sources-hive-tables.html

spark.sql("show tables").show()
spark.sql("create table hudi_cow_nonpcf_tbl ( \
  uuid int, \
  name string, \
  price double \
) using hudi").show()
spark.sql("show tables").show()
spark.sql("insert into hudi_cow_nonpcf_tbl select 1, 'a1', 20").show()
spark.sql("select * from hudi_cow_nonpcf_tbl").show()
