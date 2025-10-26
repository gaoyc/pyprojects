# encoding: utf-8
import sys
"""
首先,我们通过语句导入import
我们希望使用这一模块。模块。基本上,这句代码将转化为我们告诉 Python
sys
模块包含了与 Python 解释器及其环境相关的功能,也就是所
sys
谓的系统功能(system)。
当 Python 运行
import sys
这一语句时,它会开始寻找
模块。在这一案例中,由于其
sys
是一个内置模块,因此 Python 知道应该在哪里找到它。
如果它不是一个已编译好的模块,即用 Python 编写的模块,那么 Python 解释器将从它的
sys.path
变量所提供的目录中进行搜索。如果找到了对应模块,则该模块中的语句将在开始
运行,并能够为你所使用。在这里需要注意的是,初始化工作只需在我们第一次导入模块时
完成。
"""
print('The command line arguments are:')
for i in sys.argv:
    print(i)
print('\n\nThe PYTHONPATH is', sys.path, '\n')
