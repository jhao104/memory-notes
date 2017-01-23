
>String模块包含大量实用常量和类，以及一些过时的遗留功能，并还可用作字符串操作。

## 1. 常用方法

|  常用方法 | 描述 |
|---|---|
|  str.capitalize() | 把字符串的首字母大写 |
| str.center(width) | 将原字符串用空格填充成一个长度为width的字符串，原字符串内容居中 |
| str.count(s) | 返回字符串s在str中出现的次数 |
| str.decode(encoding='UTF-8',errors='strict') | 以指定编码格式解码字符串 |
| str.encode(encoding='UTF-8',errors='strict') | 以指定编码格式编码字符串 |
| str.endswith(s) | 判断字符串str是否以字符串s结尾 |
| str.find(s) | 返回字符串s在字符串str中的位置索引，没有则返回-1 |
| str.index(s)| 和find()方法一样，但是如果s不存在于str中则会抛出异常|
| str.isalnum() | 如果str至少有一个字符并且都是字母或数字则返回True,否则返回False|
| str.isalpha() | 如果str至少有一个字符并且都是字母则返回True,否则返回False|
| str.isdigit() | 如果str只包含数字则返回 True 否则返回 False|
| str.islower() | 如果str存在区分大小写的字符，并且都是小写则返回True 否则返回False|
| str.isspace() | 如果str中只包含空格，则返回 True，否则返回 False|
| str.istitle() | 如果str是标题化的(单词首字母大写)则返回True，否则返回False|
| str.isupper() | 如果str存在区分大小写的字符，并且都是大写则返回True 否则返回False|
| str.ljust(width) | 返回一个原字符串左对齐的并使用空格填充至长度width的新字符串 |
| str.lower() | 转换str中所有大写字符为小写|
| str.lstrip() | 去掉str左边的不可见字符|
| str.partition(s)| 用s将str切分成三个值|
| str.replace(a, b) | 将字符串str中的a替换成b|
| str.rfind(s) | 类似于 find()函数，不过是从右边开始查找|
| str.rindex(s) | 类似于 index()，不过是从右边开始|
| str.rjust(width)| 返回一个原字符串右对齐的并使用空格填充至长度width的新字符串|
| str.rpartition(s) | 类似于 partition()函数,不过是从右边开始查找|
| str.rstrip() | 去掉str右边的不可见字符|
| str.split(s) | 以s为分隔符切片str |
| str.splitlines() |  按照行分隔，返回一个包含各行作为元素的列表 |
| str.startswith(s) | 检查字符串str是否是以s开头，是则返回True，否则返回False |
| str.strip() | 等于同时执行rstrip()和lstrip()|
| str.title() | 返回"标题化"的str,所有单词都是以大写开始，其余字母均为小写|
| str.upper() | 返回str所有字符为大写的字符串 |
| str.zfill(width) |返回长度为 width 的字符串，原字符串str右对齐，前面填充0|

## 2.字符串常量

| 常数  | 含义 |
|---|---|
| string.ascii_lowercase | 小写字母'abcdefghijklmnopqrstuvwxyz'|
| string.ascii_uppercase | 大写的字母'ABCDEFGHIJKLMNOPQRSTUVWXYZ'|
| string.ascii_letters | ascii_lowercase和ascii_uppercase常量的连接串 |
| string.digits | 数字0到9的字符串:'0123456789'|
| string.hexdigits| 字符串'0123456789abcdefABCDEF'|
| string.letters| 字符串'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'|
| string.lowercase|小写字母的字符串'abcdefghijklmnopqrstuvwxyz'|
| string.octdigits| 字符串'01234567'|
| string.punctuation| 所有标点字符|
| string.printable| 可打印的字符的字符串。包含数字、字母、标点符号和空格|
| string.uppercase | 大学字母的字符串'ABCDEFGHIJKLMNOPQRSTUVWXYZ'|
| string.whitespace| 空白字符 '\t\n\x0b\x0c\r '|

## 3.字符串模板Template

通过string.Template可以为Python定制字符串的替换标准,下面是具体列子：
```
>>>from string import Template
>>>s = Template('$who like $what')
>>>print s.substitute(who='i', what='python')
i like python

>>>print s.safe_substitute(who='i') # 缺少key时不会抛错
i like $what

>>>Template('${who}LikePython').substitute(who='I') # 在字符串内时使用{}
'ILikePython'
```

Template还有更加高级的用法，可以通过继承string.Template, 重写变量delimiter(定界符)和idpattern(替换格式), 定制不同形式的模板。

```
import string

template_text = '''
    Delimiter : $de
    Replaced : %with_underscore
    Ingored : %notunderscored
'''

d = {'de': 'not replaced',
     'with_underscore': 'replaced',
     'notunderscored': 'not replaced'}


class MyTemplate(string.Template):
    # 重写模板 定界符(delimiter)为"%", 替换模式(idpattern)必须包含下划线(_)
    delimiter = '%'
    idpattern = '[a-z]+_[a-z]+'

print string.Template(template_text).safe_substitute(d)  # 采用原来的Template渲染

print MyTemplate(template_text).safe_substitute(d)  # 使用重写后的MyTemplate渲染

```

输出：
```

    Delimiter : not replaced
    Replaced : %with_underscore
    Ingored : %notunderscored


    Delimiter : $de
    Replaced : replaced
    Ingored : %notunderscored
```

可以看出原生的Template只会渲染界定符为$的情况，重写后的MyTemplate会渲染界定符为%且替换格式带有下划线的情况。





