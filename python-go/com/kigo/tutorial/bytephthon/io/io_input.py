# code=UTF-8
"""
演示用户输入
"""


def reverse(text):
    # 我们使用切片功能翻转文本。我们已经了解了我们可以通过使用 seq[a:b] 来从位置 a 开
    # 始到位置 b 结束来对序列进行切片 。我们同样可以提供第三个参数来确定切片的步长
    # （Step）。默认的步长为 1 ，它会返回一份连续的文本。如果给定一个负数步长，如 -1 ，
    # 将返回翻转过的文本。
    return text[::-1]


def is_palindrome(text):
    return text == reverse(text)


something = input("Enter text: ")
if is_palindrome(something):
    # 属于反转字符串
    print("Yes, it is a palindrome")
else:
    print("No, it is not a palindrome")

