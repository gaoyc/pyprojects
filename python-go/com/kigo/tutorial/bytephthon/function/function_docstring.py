# encoding: utf-8
"""

文档字符串(Documentation Strings)
    函数的第一行逻辑行中的字符串是该函数的 文档字符串(DocString)。这里要注意文档字符
串也适用于后面相关章节将提到的模块(Modules)与类(Class) 。
    该文档字符串所约定的是一串多行字符串,其中第一行以某一大写字母开始,以句号结束。
    第二行为空行,后跟的第三行开始是任何详细的解释说明。
    5 在此强烈建议你在你所有重要功能的所有文档字符串中都遵循这一约定。

    我们可以通过使用函数的__doc__(注意其中的双下划綫)属性(属于函数的名称)来获取函数print_max
的文档字符串属性。只消记住 Python 将所有东西都视为一个对象,这其中
自然包括函数。我们将在后面的类(Class)章节讨论有关对象的更多细节。
"""


def print_max(x, y):
    '''打印两个数值中的最大数。


         这两个数都应该是整数'''
    # 如果可能,将其转换至整数类型
    x = int(x)
    y = int(y)

    if x > y:
        print(x, 'is maximum')
    else:
        print(y, 'is maximum')


print_max(3, 5)
print(print_max.__doc__)
