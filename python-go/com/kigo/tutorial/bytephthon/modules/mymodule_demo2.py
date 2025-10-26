# encoding: utf-8

from mymodule import say_hi,__version__
"""
在这里需要注意的是,如果导入到 mymodule 中的模块里已经存在了
__version__
这一名
称,那将产生冲突。这可能是因为每个模块通常都会使用这一名称来声明它们各自的版本
号。因此,我们大都推荐最好去使用
import
语句
"""
say_hi()
print("version", __version__)