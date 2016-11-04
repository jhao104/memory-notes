    最短匹配应用于：假如有一段文本，你只想匹配最短的可能，而不是最长。
## 例子
比如有一段html片段，```<a>this is first label</a><a>the second label</a>```,如何匹配出每个a标签中的内容，下面来看下最短与最长的区别。
## 代码
```
>>> import re
>>> str = '<a>this is first label</a><a>the second label</a>'

>>> print re.findall(r'<a>(.*?)</a>', str)  # 最短匹配
['this is first label', 'the second label']

>>> print re.findall(r'<a>(.*)</a>', str)
['this is first label</a><a>the second label']
```
## 解释
例子中，模式```r'<a>(.*?)</a>```的意图是匹配被< a>和< /a>包含的文本，但是正则表达式中\*操作符是贪婪的，因此匹配操作会查找出最长的可能。
但是在*操作符后面加上？操作符，这样使得匹配变成非贪婪模式，从而得到最短匹配。