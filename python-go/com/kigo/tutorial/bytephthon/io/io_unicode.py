# encoding=utf-8
"""
# encoding=utf-8 这一注释放置在我们程序的顶端
"""
import io
f = io.open("abc.txt", "wt", encoding="utf-8")
f.write(u"Imagine non-English language here")
f.close()
text = io.open("abc.txt", encoding="utf-8").read()
print(text)