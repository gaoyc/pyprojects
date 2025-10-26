#! /bin/python2
# --*-- coding:utf-8 --*--
from pyspark.sql import SparkSession
import json

def getsparkSession():
    from pyspark import SparkConf
    conf = SparkConf
    # conf.set("xxx")
    spark = SparkSession.builder.config(conf= conf).enableHiveSupport().getOrCreate()


def row_transform(row_cells_info, hbase_structure):
    """
    这个函数是一行一行读取hbase_rdd中的record，然后将每个列里面的数据提取出来，最终形成一个dict，这个dict的结构
    大概是这样的{column_name1:value1, column_name2:value2, column_name3:value3}，如果hbase里面有些列没有值，就是
    压根没存这个字段，可以给这个字段填充一个“Null”值，以便后续可以转为dataframe格式（但是这里的“Null”就是一个字
    符串，和dataframe里面本身没有值自动默认为的“Null”是不一样的，前者在用filter这个函数是，条件要写“！=Null”，而后
    者则需要用“isNotNull()”这个函数）
    """
    row_cell_info_list =[json.loads(i) for i in row_cells_info]
    row_dict ={}
    for hbase_index in range(len(hbase_structure)):
        for cell_index in range(len(row_cell_info_list)):
            column_name = row_cell_info_list[cell_index]['qualifier']
            column_value = row_cell_info_list[cell_index]['value']
            if hbase_structure[hbase_index]== column_name:
                row_dict[column_name]= column_value.encode('utf-8')
                break
            else:
                row_dict[hbase_structure[hbase_index]]="Null"
                return row_dict


def rdd_to_df(hbase_rdd, hbase_structure):
    """
    将HBase RDD转换为DataFrame,
    这里的hbase_structure对应的是hbase中数据的列名list，如[column_name1,column_name2,column_name3]
    并且元素的顺序与hbase中列的顺序对应
    """
    # 同一个RowKey对应的列之间是用\n分割，进行split，split后每列是个dict
    print(hbase_rdd.take(50))
    data_rdd_split = hbase_rdd.map(lambda x:(x[0], x[1].split('\n')))
    # 提取列名和取值
    data_rdd_columns = data_rdd_split.map(lambda x:(x[0], row_transform(x[1], hbase_structure)))
    data = data_rdd_columns.map(lambda x:[x[0]]+[x[1][i]for i in x[1]])
    data_df = spark.createDataFrame(data,["row_key"]+ hbase_structure)
    return data_df


def hbase_read(spark,host,table,hbase_structure):
    """
    :param spark:
    :param host:
    :param table:
    :param hbase_structure:
    :return:
        读取hbase 数据转化为Saprk DataFrame
    """
    conf ={"hbase.zookeeper.quorum": host,"hbase.mapreduce.inputtable": table}
    keyConv ="org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
    valueConv ="org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"
    hbase_rdd = spark.sparkContext.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
                                                   "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                                                   "org.apache.hadoop.hbase.client.Result",
                                                   keyConverter=keyConv,
                                                   valueConverter=valueConv,
                                                   conf=conf,
                                                   batchSize=10000)
    tab = rdd_to_df(hbase_rdd, hbase_structure)
    #tab.show(10,False)
    return tab

# 二、PySpark写入Hbase，将DataFrame格式数据写入Hbase
def hbase_write(host,table,df_data):
    """
    :param host:
    :param table:
    :param df_data:
    :return:
        将Spark DataFrame 数据写入Hbase
    """
    keyConv ="org.apache.spark.examples.pythonconverters.StringToImmutableBytesWritableConverter"
    valueConv ="org.apache.spark.examples.pythonconverters.StringListToPutConverter"
    conf ={"hbase.zookeeper.quorum": host,"hbase.mapred.outputtable": table,
           "mapreduce.outputformat.class":"org.apache.hadoop.hbase.mapreduce.TableOutputFormat",
           "mapreduce.job.output.key.class":"org.apache.hadoop.hbase.io.ImmutableBytesWritable",
           "mapreduce.job.output.value.class":"org.apache.hadoop.io.Writable"}
    # DataFrame转换为rdd写入hbase
    col_list = df_data.columns
    print(col_list)
    rdd_data = df_data.rdd.map(lambda x:(x["row_key"],((i,x[i])for i in col_list[1:])))
    rdd_data = rdd_data.flatMapValues(lambda x:x)
    rrd2 = rdd_data.map(lambda x:(x[0],[x[0],'cf1',x[1][0],x[1][1]]))
    print(rrd2.take(10))
    rrd2.saveAsNewAPIHadoopDataset(conf=conf,keyConverter=keyConv,valueConverter=valueConv)


if __name__ =="__main__":
    """
    执行测试代码
    """
    spark = SparkSession.Builder().appName("Demo_SparkHbase_read_write").getOrCreate()
    # 创建spark对象print('spark对象已创建')
    host ='127.1.1.1'
    # 定了两个同结构的表，方便测试 ，表列簇为cf1 ,
    table ='test'
    table01 ='test_01'
    # 将 rdd格式转换成dataframe格式，定义使用的表的结构，不用的列可以不指名，
    hbase_structure =["age","name"]
    # 读取Hbase表数据转换为Spark dataframe格式
    df_data = hbase_read(spark,host,table,hbase_structure)
    df_data.show(10,False)
    # 借用上面的DataFrame数据集导入到另外一张表中
    hbase_write(host,table01,df_data)
    spark.stop()


"""
執行程序
    spark2 - submit - -master
    yarn \--executor - memory
    1
    G \--executor - cores
    1 \--num - executors
    1 \--jars
    "/home/xxxx/jars/spark-examples_2.11-1.6.0-typesafe-001.jar" \ / home / xxxx / test / Demo_SparkHbase_read_write.py
"""
