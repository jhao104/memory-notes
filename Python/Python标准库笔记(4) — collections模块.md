>这个模块提供几个非常有用的Python容器类型

## 1.容器

| 名称  | 功能描述 |
|---|---|
| OrderedDict  | 保持了key插入顺序的dict |
| namedtuple |  生成可以使用名字来访问元素内容的tuple子类|
| Counter | 计数器，主要用来计数 |
| deque | 类似于list的容器，可以快速的在队列头部和尾部添加、删除元素|
| defaultdict | dict的子类，带有默认值的字典|

## 2.OrderedDict

　　`OrderedDict`类似于正常的词典，只是它记住了元素插入的顺序，当迭代它时，返回它会根据插入的顺序返回。

* 和正常字典相比,它是"有序"的(插入的顺序)。

```python
from collections import OrderedDict

dict1 = dict()  # 普通字典
dict1['apple'] = 2
dict1['banana'] = 1
dict1['orange'] = 3

dict2 = OrderedDict()  # 有序字典
dict2['apple'] = 2
dict2['banana'] = 1
dict2['orange'] = 3

for key, value in dict1.items():
    print 'key:', key, ' value:', value

for key, value in dict2.items():
    print 'key:', key, ' value:', value
```
````shell
# ----输出结果-----

# 普通字典
key: orange  value: 3
key: apple  value: 2
key: banana  value: 1

# 有序字典
key: apple  value: 2
key: banana  value: 1
key: orange  value: 3
````

* 如果重写已经存在的key，原始顺序保持不变，如果删除一个元素再重新插入，那么它会在末尾。

```python
from collections import OrderedDict

dict2 = OrderedDict()
dict2['apple'] = 2
dict2['banana'] = 1
dict2['orange'] = 3

# 直接重写apple的值,顺序不变
dict2['apple'] = 0

# 删除在重新写入banana, 顺序改变
dict2.pop('banana')
dict2['banana'] = 1

print dict2
```

```shell
# ----输出结果-----
OrderedDict([('apple', 0), ('orange', 3), ('banana', 1)])
```

* 可以使用排序函数，将普通字典变成OrderedDict。

```python
from collections import OrderedDict

d = {'banana': 3, 'apple': 4, 'pear': 1, 'orange': 2}
order_d = OrderedDict(sorted(d.items(), key=lambda t: t[1]))

for key, value in order_d.items():
    print 'key:', key, ' value:', value
```

```shell
# ----输出结果-----
key: pear  value: 1
key: orange  value: 2
key: banana  value: 3
key: apple  value: 4
```

## 3.namedtuple

　　namedtuple就是命名的tuple，一般情况下的tuple是这样的(item1, item2, item3,...)，所有的item都只能通过index访问，没有明确的称呼，而namedtuple就是事先把这些item命名，以后可以方便访问。

```python
from collections import namedtuple

# 定义一个namedtuple类型User，并包含name，sex和age属性。
User = namedtuple('User', ['name', 'sex', 'age'])

# 创建一个User对象
user1 = User(name='name1', sex='male', age=18)

# 也可以通过一个list来创建一个User对象，这里注意需要使用"_make"方法
user2 = User._make(['name2', 'male', 21])

print 'user1:', user1

# 使用点号获取属性
print 'name:', user1.name, ' sex:', user1.sex, ' age:', user1.age

# 将User对象转换成字典，注意要使用"_asdict"
print 'user1._asdict():', user1._asdict()

# 字典转换成namedtuple
name_dict = {'name': 'name3', 'sex': 'male', 'age': 20}
print 'dict2namedtuple:', User(**name_dict)

# 修改对象属性，注意要使用"_replace"方法
print 'replace:', user1._replace(age=22)
```

```shell
# ----输出结果-----
user1: User(name='name1', sex='male', age=18)
name: name1  sex: male  age: 18
user1._asdict(): OrderedDict([('name', 'name1'), ('sex', 'male'), ('age', 18)])
dict2namedtuple: User(name='name3', sex='male', age=20)
replace: User(name='name1', sex='male', age=22)
```

## 4.Counter

　　Counter类的目的是用来跟踪值出现的次数。它是一个无序的容器类型，以字典的键值对形式存储，其中元素作为key，其计数作为value。

* Counter创建有如下几种方法

```python
from collections import Counter

print Counter('aabbcccd')  # 从一个可iterable对象（list、tuple、dict、字符串等）创建
print Counter(['a', 'a', 'c'])  # 从一个可iterable对象（list、tuple、dict、字符串等）创建
print Counter({'a': 4, 'b': 2})  # 从一个字典对象创建
print Counter(a=4, b=2)  # 从一组键值对创建
```

```shell
# ----输出结果-----
Counter({'c': 3, 'a': 2, 'b': 2, 'd': 1})
Counter({'a': 2, 'c': 1})
Counter({'a': 4, 'b': 2})
Counter({'a': 4, 'b': 2})
```

* 获取元素的计数时和dict类似, 但是这里的key不存在时返回0，而不是KeyError

```python
>>> c = Counter("acda")
>>> c["a"]
2
>>> c["h"]
0
```

* 可以使用update和subtract对计数器进行更新(增加和减少)

```python
from collections import Counter

c = Counter('aaabbc')

print 'c:', c

c.update("abc")
print 'c.update("abc"):', c  # 用另一个iterable对象update 也可传入一个Counter对象

c.subtract("abc")
print 'c.subtract("abc"):', c  # 用另一个iterable对象subtract 也可传入一个Counter对象
```

```shell
# ----输出结果-----
c: Counter({'a': 3, 'b': 2, 'c': 1})
c.update("abc"): Counter({'a': 4, 'b': 3, 'c': 2})
c.subtract("abc"): Counter({'a': 3, 'b': 2, 'c': 1})
```

* 返回计数次数top n的元素

```python
from collections import Counter

c = Counter('aaaabbcccddeeffg')

print c.most_common(3)
```

```shell
# ----输出结果-----
[('a', 4), ('c', 3), ('b', 2)]
```

* Counter还支持几个为数不多的数学运算+、-、&、|

```python
from collections import Counter

a = Counter(a=3, b=1)  
b = Counter(a=1, b=1)

print 'a+b:', a + b  # 加法,计数相加
print 'a-b:', a - b  # 减法,计数相减
print 'b-a:', b - a  # 只保留正计数
print 'a&b:', a & b  # 交集
print 'a|b:', a | b  # 并集
```

```shell
# ----输出结果-----
a+b: Counter({'a': 4, 'b': 2})
a-b: Counter({'a': 2})
b-a: Counter()
a&b: Counter({'a': 1, 'b': 1})
a|b: Counter({'a': 3, 'b': 1})
```

## 5.deque

　　deque就是双端队列，是一种具有队列和栈的性质的数据结构，适合于在两端添加和删除，类似与序列的容器

* 常用方法

```python
from collections import deque

d = deque([])  # 创建一个空的双队列

d.append(item)  # 在d的右边(末尾)添加项目item

d.appendleft(item)  # 从d的左边(开始)添加项目item

d.clear()  # 清空队列,也就是删除d中的所有项目

d.extend(iterable)  # 在d的右边(末尾)添加iterable中的所有项目

d.extendleft(item)  # 在d的左边(开始)添加item中的所有项目

d.pop()  # 删除并返回d中的最后一个(最右边的)项目。如果d为空，则引发IndexError

d.popleft()  # 删除并返回d中的第一个(最左边的)项目。如果d为空，则引发IndexError

d.rotate(n=1)
# 将d向右旋转n步(如果n<0,则向左旋转)

d.count(n)  # 在队列中统计元素的个数，n表示统计的元素

d.remove(n)  # 从队列中删除指定的值

d.reverse()  # 翻转队列
```

## 6.defaultdict

　　使用dict时，如果引用的Key不存在，就会抛出`KeyError`。如果希望key不存在时，返回一个默认值，就可以用defaultdict

* 比如要统计字符串中每个单词的出现频率

```python
from collections import defaultdict

s = 'ilikepython'

# 使用普通字典
frequencies = {}
for each in s:
    frequencies[each] += 1

# 使用普通字典
frequencie = defaultdict(int)
for each in s:
    frequencie[each] += 1
```

　　第一段代码中会抛出一个`KeyError`的异常,而使用defaultdict则不会。defaultdict也可以接受一个函数作为参数来初始化:

```python
>>> from collections import defaultdict
>>> d = defaultdict(lambda : 0)
>>> d['0']
0
```

