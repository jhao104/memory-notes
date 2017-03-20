　　re模块提供了一系列功能强大的正则表达式(regular expression)工具，它们允许你快速检查给定字符串是否与给定的模式匹配(match函数), 或者包含这个模式(search函数)。正则表达式是以紧凑(也很神秘)的语法写出的字符串模式。

## 1. 常用方法

|  常用方法 | 描述 |
|---|---|
| match(pattern, string, flags=0) |如果字符串string的开头和正则表达式pattern匹配返回相应的MatchObject的实例，否则返回None|
| search(pattern, string, flags=0) | 扫描string，如果有个位置可以匹配正则表达式pattern，就返回一个MatchObject的实例，否则返回None |
| sub(pattern, repl, string, count=0, flags=0)| 将string里匹配pattern的部分，用repl替换掉，最多替换count次|
| subn(pattern, repl, string, count=0, flags=0)| 和sub类似，subn返回的是一个替换后的字符串和匹配次数组成的元组|
| split(pattern, string, maxsplit=0, flags=0)| 用pattern匹配到的字符串来分割string |
| findall(pattern, string, flags=0) | 以列表的形式返回string里匹配pattern的字符串 |
| compile(pattern, flags=0)compile(pattern, flags=0) | 把一个正则表达式pattern编译成正则对象，以便可以用正则对象的match和search方法 |
| purge()| Clear the regular expression cache |
| escape(string)| 把string中除了字母和数字以外的字符，都加上反斜杆 |

## 2. 特殊匹配符

| 语法  | 说明
|---|---|
| .  | 匹配除了换行符外的任何字符 |
| ^  | 头匹配 |
| $ | 尾匹配 |
| * | 匹配前一个字符0次或多次|
| + | 匹配前一个字符1次或多次|
| ? | 匹配前一个字符0次或一次|
| {m,n} | 匹配前一个字符m至n次|
| \ |对任一特殊字符进行转义|
| [] |用来表示一个字符集合|
| \| |或,代表左右任意匹配一个|

## 3. 模块方法

### re.match(pattern, string, flags=0)

　　从字符串的开始匹配，如果pattern匹配到就返回一个Match对象实例(Match对象在后面描述)，否则放回None。flags为匹配模式(会在下面描述)，用于控制正则表达式的匹配方式。
```python
import re

a = 'abcdefg'
print re.match(r'abc', a)  # 匹配成功
print re.match(r'abc', a).group()
print re.match(r'cde', a)  # 匹配失败

>>><_sre.SRE_Match object at 0x0000000001D94578>
>>>abc
>>>None

```

### search(pattern, string, flags=0)

　　用于查找字符串中可以匹配成功的子串，如果找到就返回一个Match对象实例,否则返回None。
```python
import re

a = 'abcdefg'
print re.search(r'bc', a)
print re.search(r'bc', a).group()
print re.search(r'123', a)

>>><_sre.SRE_Match object at 0x0000000001D94578>
>>>bc
>>>None
```

### sub(pattern, repl, string, count=0, flags=0)

　　替换，将string里匹配pattern的部分，用repl替换掉，最多替换count次（剩余的匹配将不做处理），然后返回替换后的字符串。
```python
import re

a = 'a1b2c3'
print re.sub(r'\d+', '0', a)  # 将数字替换成'0'
print re.sub(r'\s+', '0', a)  # 将空白字符替换成'0'

>>>a0b0c0
>>>a1b2c3
```

### subn(pattern, repl, string, count=0, flags=0)

　　跟sub()函数一样，只是它返回的是一个元组，包含新字符串和匹配到的次数

```python
import re

a = 'a1b2c3'
print re.subn(r'\d+', '0', a)  # 将数字替换成'0'

>>>('a0b0c0', 3)
```

### split(pattern, string, maxsplit=0, flags=0)

　　正则版的split(),用匹配pattern的子串来分割string，如果pattern里使用了圆括号，那么被pattern匹配到的串也将作为返回值列表的一部分,maxsplit为最多被分割的字符串。

```python
import re

a = 'a1b1c'
print re.split(r'\d', a)
print re.split(r'(\d)', a)

>>>['a', 'b', 'c']
>>>['a', '1', 'b', '1', 'c']
```

### findall(pattern, string, flags=0)

　　以列表的形式返回string里匹配pattern的不重叠的子串。

```python
import re

a = 'a1b2c3d4'
print re.findall('\d', a)

>>>['1', '2', '3', '4']
```

## 4. Match对象

　　re.match()、re.search()成功匹配的话都会返回一个Match对象，它包含了很多此次匹配的信息，可以使用Match提供的属性或方法来获取这些信息。例如：
```
>>>import re

>>>str = 'he has 2 books and 1 pen'
>>>ob = re.search('(\d+)', str)

>>>print ob.string  # 匹配时使用的文本
he has 2 books and 1 pen

>>>print ob.re # 匹配时使用的Pattern对象
re.compile(r'(\d+)')

>>>print ob.group()  # 获得一个或多个分组截获的字符串
2

>>>print ob.groups()  # 以元组形式返回全部分组截获的字符串
('2',)

```

## 5.Pattern对象

　　Pattern对象对象由re.compile()返回，它带有许多re模块的同名方法，而且方法作用类似一样的。例如:
```python
>>>import re
>>>pa = re.compile('(d\+)')

>>>print pa.split('he has 2 books and 1 pen')
['he has ', '2', ' books and ', '1', ' pen']

>>>print pa.findall('he has 2 books and 1 pen')
['2', '1']

>>>print pa.sub('much', 'he has 2 books and 1 pen')
he has much books and much pen
```

## 6.匹配模式

　　匹配模式取值可以使用按位或运算符'|'表示同时生效，比如re.I | re.M, 下面是常见的一些flag。

* re.I(re.IGNORECASE): 忽略大小写

```python
>>>pa = re.compile('abc', re.I)
>>>pa.findall('AbCdEfG')
>>>['AbC']
```

* re.L(re.LOCALE)：字符集本地化

　　这个功能是为了支持多语言版本的字符集使用环境的，比如在转义符`\w`，在英文环境下，它代表`[a-zA-Z0-9]`，即所以英文字符和数字。如果在一个法语环境下使用，有些法语字符串便匹配不上。加上这L选项和就可以匹配了。不过这个对于中文环境似乎没有什么用，它仍然不能匹配中文字符。

* re.M(re.MULTILINE): 多行模式，改变'^'和'$'的行为

```python
>>>pa = re.compile('^\d+')
>>>pa.findall('123 456\n789 012\n345 678')
>>>['123']

>>>pa_m = re.compile('^\d+', re.M)
>>>pa_m.findall('123 456\n789 012\n345 678')
>>>['123', '789', '345']
```


* re.S(re.DOTALL): 点任意匹配模式，改变'.'的行为

　　`.`号将匹配所有的字符。缺省情况下`.`匹配除换行符`\n`外的所有字符，使用这一选项以后，点号就能匹配包括换行符的任何字符。

* re.U(re.UNICODE): 根据Unicode字符集解析字符

* re.X(re.VERBOSE): 详细模式

```python
# 这个模式下正则表达式可以是多行，忽略空白字符，并可以加入注释。以下两个正则表达式是等价的
a = re.compile(r"""\d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.X)
b = re.compile(r"\d+\.\d*")
# 但是在这个模式下，如果你想匹配一个空格，你必须用'/ '的形式（'/'后面跟一个空格）
```