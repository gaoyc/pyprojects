# encoding: utf-8
"""
列表
是一种用于保存一系列有序项目的集合.
项目的列表应该用方括号括起来
可以添加、移除或搜索列表中的项目。既然我们可以添加或删除项目,我们会说列表是一种可变的(Mutable)数据类型,意即,这种类型是可以被改变的。
"""

# this is my shopping list
shoplist = ['apple', 'mango', 'carrot', 'banana']

print('I have', len(shoplist), 'items to purchase.')

# end=' '是使用命名参数, 函数参数end的值为空格
print('These items are:', end=' ')
for item in shoplist:
    print(item, end=' ')

print('\nI also have to buy rice.')
shoplist.append('rice')
print('My shopping list is now', shoplist)

print('I will sort my list now')
shoplist.sort()
print('Sorted shopping list is', shoplist)

print('The first item I will buy is', shoplist[0])
olditem = shoplist[0]
del shoplist[0]
print('I bought the', olditem)
print('My shopping list is now', shoplist)
