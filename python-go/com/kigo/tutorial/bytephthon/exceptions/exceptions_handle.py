"""
异常处理
我们可以通过使用 try..except 来处理异常状况。一般来说我们会把通常的语句放在 try 代
码块中，将我们的错误处理器代码放置在 except 代码块中。
"""

try:
    text = input('Enter something --> ')
except EOFError:
    print('Why did you do an EOF on me?')
except KeyboardInterrupt:
    print('You cancelled the operation.')
else:
    print('You entered {}'.format(text))
