## 简介

官方描述：Functional tools for creating and using iterators.即用于创建高效迭代器的函数。

## itertools.chain(*iterable) 

将多个序列作为一个单独的序列返回。
例如：
```
import itertools
for each in itertools.chain('i', 'love', 'python'):
    print each
```
输出：
```
i
l
o
v
e
p
y
t
h
o
n
```

## itertools.combinations(iterable, r)

返回指定长度的"组合"
例如：
```
import itertools
for each in itertools.combinations('abc', 2):
    print each
```
输出：
```
('a', 'b')
('a', 'c')
('b', 'c')
```

## itertools.combinations_with_replacement(iterable, r)

返回指定长度的“组合”，组合内元素可重复
例如：
```
import itertools
for each in itertools.combinations_with_replacement('abc', 2):
    print each
```
输出：
```
('a', 'a')
('a', 'b')
('a', 'c')
('b', 'b')
('b', 'c')
('c', 'c')
```

## itertools.product(*iterable[,repeat])

返回指定长度的所有组合，可理解为笛卡尔乘积
例如：
```
import itertools
for each in itertools.product('abc', repeat=2):
    print each
```
('a', 'a')
('a', 'b')
('a', 'c')
('b', 'a')
('b', 'b')
('b', 'c')
('c', 'a')
('c', 'b')
('c', 'c')

## itertools.premutations(iteravle[,r])

返回长度为r的排列
例如：
```
import itertools
for value in itertools.permutations('abc', 2):
    print value
```
输出：
```
('a', 'b')
('a', 'c')
('b', 'a')
('b', 'c')
('c', 'a')
('c', 'b')
```

## itertools.compress(data,selector)

返回selector为True的data对应元素
例如：
```
import itertools
for each in itertools.compress('abcd', [1, 0, 1, 0]):
    print each
```
输出：
```
a
c
```

## itertools.count(start=0,step=1)

返回以start开始，step递增的序列，无限递增
例如：
```
import itertools
for each in itertools.count(start=0, step=2):
    print each
```
输出：
```
1
2
3
.
.
```
## itertools.cycle(iterable)

将迭代器进行无限迭代
例如：
```
import itertools
for each in itertools.cycle('ab'):
    print each
```
输出：
```
a
b
a
b
.
.
```

## itertools.dropwhile(predicate, iterable)

直到predicate为真，就返回iterable后续数据， 否则drop掉
例如：
```
import itertools
for each in itertools.dropwhile(lambda x: x<5, [2,1,6,8,2,1]):
    print each
```

输出：
```
6
8
2
1
```

## itertools.groupby(iterable[,key])

返回一组（key,itera）,key为iterable的值，itera为等于key的所有项
例如:
```
import itertools
for key, vale in itertools.groupby('aabbbc'):
    print key, list(vale)
```
输出:
```
a ['a', 'a']
b ['b', 'b', 'b']
c ['c']
```

## itertools.ifilter(predicate, iterable)

返回predicate结果为True的元素迭代器，如果predicate为None,则返回所有iterable中为True的项
例如：
```
import itertools
for value in itertools.ifilter(lambda x: x % 2, range(10)):
    print value
```
输出:
```
1
3
5
7
9
```

## itertools.ifilterfasle(predicate,iterable)

返回predicate为False的元素，如果predicate为None,则返回所有iterable中为False的项
例如：
```
import itertools
for value in itertools.ifilterfalse(lambda x: x % 2, range(10)):
    print value
```
输出:
```
0
2
4
6
8
```

## itertools.imap(function,*iterables)

相当于迭代器方式的map()
例如：
```
import itertools
for value in itertools.imap(lambda x, y: x+y, (1,2,3), (4,5,6)):
    print value
```
输出:
```
5
7
9
```

## itertools.islice(iterable, start,stop[,step])

相当于迭代器方式的切片操作
例如：
```
import itertools
for value in itertools.islice('abcdefg', 1, 4, 2):
    print value
```
输出:
```
b
d
```

## itertools.repeat(object,[,times])

不停的返回object对象，如果指定了times,则返回times次
例如：
```
import itertools
for value in itertools.repeat('a', 2):
    print value
```
输出:
```
a
a
```

## itertools.starmap(function,iterable)

返回function(iter)的值，iter为iterable的元素
例如：
```
import itertools
for value in itertools.starmap(lambda x, y: x * y, [(1, 2), (3, 4)]):
    print value
```
输出:
```
2
12
```

## itertools.takewhile(predicate,iterable)

如果predicate为真，则返回iterable元素，如果为假则不再返回，break.
例如：
```
import itertools
for value in itertools.takewhile(lambda x: x < 5, [1, 3, 5, 6]):
    print value
```
输出:
```
1
3
```