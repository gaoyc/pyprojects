# encoding=utf-8
import time

from pyspark.context import SparkContext

# 时间差距，用以计算指定时间的前后开始、结束时间
timediff = 12 * 3600 * 1000
tableName = "tb_test54y_carbondata"


def format2sql(line):
    # 数据样例如下:
    # 460000036584678|++|15945231328|++|86000042538295|++|92|++|92|++|97092|++|rstuv|xyzabcdef|++|mnopq|stuv|++|440103194000097092|++|2|++|497092|++|497092|++|1557169199|++|速度很慢美报不出所料几行字志摩
    values = line.split("|++|")
    if len(values) >= 12:
        c1 = values[0]
        time = int(values[12])
        beginstamp = time - timediff
        endstamp = time + timediff
        return "select * from %s  where C1='%s' and C35 >= %d  and C35< %d" % (tableName, c1, beginstamp, endstamp)


def gendcsql(inpath, outpath, num=100):
    sc = SparkContext(appName="gensamplesql4file")
    # sc = SparkContext("local", "gensamplesql4file")
    lines = sc.textFile(inpath)

    # samplesrdd = lines.sample(False, num)
    # sqlrdd = samplesrdd.map(lambda x: format2sql(x)).filter(lambda x: len(x) > 0)

    # 若为true，表示会将抽到的样例重新放回去继续抽样，当指定抽样条数大于样本总数是，也会返回足够的指定条数
    samples = lines.takeSample(True, num)
    sqlstmp = [format2sql(x) for x in samples]
    # sqls = list(filter(lambda x: x is not None, sqlstmp))
    sqls = list(filter(None, sqlstmp))
    sc.parallelize(sqls).coalesce(1).saveAsTextFile(outpath)



def testformat2sql():
    line = "460000036584678|++|15945231328|++|86000042538295|++|92|++|92|++|97092|++|rstuv|xyzabcdef|++|mnopq|stuv|++|440103194000097092|++|2|++|497092|++|497092|++|1557169199|++|速度很慢美报不出所料几行字志摩"
    ret = format2sql(line)
    print(ret)
    line = ""
    ret = format2sql(line)
    print(ret)


if __name__ == '__main__':
    outtime = time.strftime("%Y%m%d%H%M%S", time.localtime())

    inpath = "E:/gyc/task-工作任务/3-方案测试类/1-testData/henanmpp-生成测试数据/TB_HN_BIGTABLE.V003.20190505_0.LteTrans1.0-head-10w"
    outpath = "file:///D:/tmp/dcsql/sql-%s" % outtime
    # inpath = "/testdata/TB_HN_BIGTABLE/new/TB_HN_BIGTABLE.V003.20190505_0.LteTrans1.0"
    # inpath = "/testdata/TB_HN_BIGTABLE/*/TB_HN_BIGTABLE*"
    # outpath = "/tmp/out/sql/sql-%s" % outtime

    gendcsql(inpath, outpath, 10)
    print("=================finish! outpath=%s" % outpath)

