
## 在pycharm或直接在pyspark shell环境中执行如下测试代码报错：pyspark3.1: Python worker failed to connect back

- 解决方法
win10增加系统环境变量：
```
PYSPARK_PYTHON=python
```

主要是指定PYSPARKS使用的python命令，linux可使用which python查看，window可使用where python查看。

问题成功解决！！！