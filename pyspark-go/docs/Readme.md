
## 运行配置

注意：
spark-2.4.5最高python3.7，与python3.8有兼容性问题，python3.8需要spark3.x才适配

## pycham运行调试spark程序

前提:
系统配置好JDK

### 方式一: 使用pip安装的spark

pip install pyspark==version-x

然后在直接运行spark py文件

### 方式一: 运行配置使用外部spark安装部署包

Run/Debug Configurations => Enviroment variables 增加配置如下环境变量
```properties
SPARK_HOME=E:\deploy\spark\spark-2.3.4-bin-hadoop2.7
PYSPARK_PYTHON=python
PYTHONUNBUFFERED=1
```




