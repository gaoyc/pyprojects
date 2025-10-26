"""
__init__ 方法会在类的对象被实例化（Instantiated）时立即运行。这一方法可以对任何你想
进行操作的目标对象进行初始化（Initialization）操作。这里你要注意在 init 前后加上的双下
划线。
"""


class Person:
    def __init__(self, name):
        self.name = name
        """
        在这里，我们创建了一个字段，同样称为 name 。要注意到尽管它们的名字都是“name”，但这是
两个不相同的变量。虽说如此，但这并不会造成任何问题，因为 self.name 中的点号意味着
这个叫作“name”的东西是某个叫作“self”的对象的一部分，而另一个 name 则是一个局部变
量。
        """

    def say_hi(self):
        print("hello, my name is", self.name)


p = Person("Kigo")
p.say_hi()
# 前面两行同时也能写作
# Person('Swaroop').say_hi()
