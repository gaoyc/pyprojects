"""
列表推导
列表推导（List Comprehension）用于从一份现有的列表中得到一份新列表。想象一下，现在
你已经有了一份数字列表，你想得到一个相应的列表，其中的数字在大于 2 的情况下将乘以
2。列表推导就是这类情况的理想选择。
"""

listone = [2, 3, 4]
listtwo = [2*i for i in listone if i > 2]
print(listtwo)