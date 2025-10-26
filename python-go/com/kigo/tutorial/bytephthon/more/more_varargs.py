"""
在函数中接收元组与字典
有一种特殊方法，即分别使用 * 或 ** 作为元组或字典的前缀，来使它们作为一个参数为
函数所接收。当函数需要一个可变数量的实参时，这将颇为有用。

因为我们在 args 变量前添加了一个 * 前缀，函数的所有其它的额外参数都将传递到
args 中，并作为一个元组予以储存。如果采用的是 ** 前缀，则额外的参数将被视为字典
的键值—值配对。
"""


def powersum(power, *args):
    '''Return the sum of each argument raised to the specified power.'''
    total = 0
    for i in args:
        total += pow(i, power)
    return total


print(powersum(2, 3, 4))
print(powersum(2, 10))
