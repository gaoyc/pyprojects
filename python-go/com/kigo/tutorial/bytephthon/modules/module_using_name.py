# encoding: utf-8
"""
模块的__name__
每个模块都有一个名称,而模块中的语句可以找到它们所处的模块的名称。
每一个 Python 模块都定义了它的__name__属性。如果它与__main__属性相同则代表这一模块是由用户独立运行的,因此我们便可以采取适当的行动。
"""

if __name__ == '__main__':
    print('This program is being run by itself')
else:
    print('I am being imported from another module')

"""
$ python
>>> import module_using_name
I am being imported from another module
>>>
"""