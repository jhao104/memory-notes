> itertools 用于更高效地创建迭代器的函数工具。

`itertools` 提供的功能受Clojure，Haskell，APL和SML等函数式编程语言的类似功能的启发。它们的目的是快速有效地使用内存，并且将它们关联在一起以表示更复杂的基于迭代的算法。

基于迭代器的代码比使用列表的代码提供了更好的内存消耗特性。因为直到数据需要使用时才从迭代器中生成，所有数据不需要同时存储在内存中。这种 `“惰性”` 的处理模式可以减少大型数据集的交换和其他副作用，从而提高性能。

除了 `itertools` 中定义的函数之外，本文中的示例还使用了一些内置函数进行迭代。

### 1.合并和分割

`chain()` 函数将多个迭代器作为参数，并返回一个迭代器，这样它生成所有输入的内容，就像来自于单个迭代器一样。

```python
from itertools import chain

for i in chain([1, 2, 3], ['a', 'b', 'c']):
    print(i, end=' ')
```

使用 `chain()` 可以轻松地处理多个序列，而不需要生成一个更大的序列。

```python
# OutPut
1 2 3 a b c 
```

如果要组合的迭代不是全部预先显式声明的，或者需要惰性计算的，则可以使用 `chain.from_iterable()` 来替换 `chain()` 。
```python
from itertools import chain

def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ['a', 'b', 'c']

for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=' ')
```

```python
# OutPut
1 2 3 a b c 
```

Python内置函数 `zip()` 也是返回一个迭代器，但它是将几个迭代器的元素组合成元组。
```python
for i in zip([1, 2, 3], ['a', 'b', 'c']):
    print(i)
```

`zip()` 和本模块中的其他函数一样，返回一个可迭代的对象，每次迭代产生一个值。
```python
# OutPut
(1, 'a')
(2, 'b')
(3, 'c')
```

但是, 使用 `zip()` 时当第一个输入迭代器耗尽时，`zip()` 就会停止。如果要处理所有的输入，即使迭代器产生不同数量的值，那么可以使用 `zip_longest()` 。
```python
from itertools import zip_longest

r1 = range(3)
r2 = range(2)

print('使用zip会提前结果迭代:')
print(list(zip(r1, r2)))
print()
print('zip_longest会处理完所有值:')
print(list(zip_longest(r1, r2)))
```

默认情况下，`zip_longest()` 会使用 `None` 来填充缺失位置的值。使用 `fillvalue` 参数来设置不同的替代值。
```python
# OutPut
使用zip会提前结果迭代:
[(0, 0), (1, 1)]

zip_longest会处理完所有值:
[(0, 0), (1, 1), (2, None)]
```

`islice()` 函数返回一个迭代器，用于通过索引返回输入迭代器的指定项。
```python
from itertools import islice

print('Stop at 5:')
for i in islice(range(100), 5):
    print(i, end=' ')
print()

print('Start at 5, Stop at 10:')
for i in islice(range(100), 5, 10):
    print(i, end=' ')
print()

print('By tens to 100:')
for i in islice(range(100), 0, 100, 10):
    print(i, end=' ')
print()
```

`islice()` 接收和列表切片相同的参数：`start` ， `stop` 和 `step` 。 `start` 和 `step` 参数是可选的。

```python
# OutPut
Stop at 5:
0 1 2 3 4 
Start at 5, Stop at 10:
5 6 7 8 9 
By tens to 100:
0 10 20 30 40 50 60 70 80 90 
```

`tee()` 函数作用是根据单个原始输入返回多个独立的迭代器（默认为两个）。
```python
from itertools import islice, tee

r = islice(range(10), 5)
i1, i2 = tee(r)

print('i1:', list(i1))
print('i2:', list(i2))
```

`tee()` 具有与Unix `tee` 实用程序类似的语义，它从它的输入中重复地读取的值并将它们写入一个命名文件和标准输出。 通过 `tee()` 函数可以将同一组数据提供给多个算法并行处理。
```python
# OutPut
i1: [0, 1, 2, 3, 4]
i2: [0, 1, 2, 3, 4]
```

需要注意,由 `tee()` 创建的新迭代器将共享它们的输入，因此在创建新迭代器后不要再使用输入的迭代器。

```python
from itertools import islice, tee

r = islice(range(10), 5)
i1, i2 = tee(r)

print('迭代原始:', end=' ')
for i in r:
    print(i, end=' ')
    if i > 1:
        break
print()

print('i1:', list(i1))
print('i2:', list(i2))
```

如果原始迭代器已经消耗了一些值，那么新的迭代器将不会生成这些值。
```python
# OutPut
迭代原始: 0 1 2
i1: [3, 4]
i2: [3, 4]
```

### 2.计算输入

Python内置的 `map()` 函数返回一个迭代器。 该迭代器根据输入迭代器中的值调用函数，并返回结果。当任意一个输入迭代器耗尽时它就立刻停止。
```python
def times_two(x):
    return 2 * x

def multiply(x, y):
    return (x, y, x * y)

print('单个输入:')
for i in map(times_two, range(5)):
    print(i, end=' ')

print('\n多个输入:')
r1 = range(5)
r2 = range(5, 10)
for i in map(multiply, r1, r2):
    print('{:d} * {:d} = {:d}'.format(*i))

print('\n迭代停止:')
r1 = range(5)
r2 = range(2)
for i in map(multiply, r1, r2):
    print(i)
```

在第一个例子中，函数将所有输入值乘以2。在第二个例子中，函数将从两个单独的迭代器中获取的两个参数相乘，并返回一个包含原始参数和计算值的元组。第三个例子中，在生成了两个元组之后便停止了，因为第二个输入已经耗尽。

```python
# OutPut
单个输入:
0 2 4 6 8
多个输入:
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36

迭代停止:
(0, 0, 0)
(1, 1, 1)
```

`starmap()` 函数与 `map()` 类似，但不是从多个迭代器构造元组，而是使用 `*` 语法将单个迭代器中的项作为参数解包给map函数。
```python
from itertools import starmap

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

for i in starmap(lambda x, y: (x, y, x * y), values):
    print('{} * {} = {}'.format(*i))
```

如果使用 `map()` 函数将是这种调用 `f(i1,i2)` ，而使用 `starmap()` 直接是 `f(*i)` 。
```python
#OutPut
0 * 5 = 0
1 * 6 = 6
2 * 7 = 14
3 * 8 = 24
4 * 9 = 36
```
### 3.产生新值

`count()` 函数会返回一个可以无限地产生连续整数的迭代器。第一个数字可以作为参数传递(默认值为0)。没有上限参数(有关对结果集的更多控制，请参阅内置的 `range()`)。
```python
from itertools import count

for i in zip(count(1), ['a', 'b', 'c']):
    print(i)
```

此示例因为使用了 `zip()` 和有限长度列表参数所以才停止。
```python
# OutPut
(1, 'a')
(2, 'b')
(3, 'c')
```

`count()` 的start和step参数可以是任何可以加在一起的数字值。
```python
import fractions
from itertools import count

start = fractions.Fraction(1, 3)
step = fractions.Fraction(1, 3)

for i in zip(count(start, step), ['a', 'b', 'c']):
    print('{}: {}'.format(*i))
```

本例中，起始点和步长来自 `Fraction` （分数）模块的 `fraction` 对象。
```python
# OutPut
1/3: a
2/3: b
1: c
```

`cycle()` 函数的作用是:返回一个迭代器，该迭代器重复无限地给出的参数的内容。因为它必须记住输入迭代器的全部内容，所以如果迭代器很长，它可能会消耗相当多的内存。
```python
from itertools import cycle

for i in cycle(['a', 'b', 'c']):
    print(i)
```

如果没有打断，它会无限循环下去。
```python
# OutPut
a
b
c
a
b
...
```

`repeat()` 函数的作用是:返回一个迭代器，该迭代器每次访问时都会产生相同的值。
```python
from itertools import repeat

for i in repeat('over-and-over', times=5):
    print(i)
```

`repeat()` 返回的迭代器将不断返回数据，除非提供可选的times参数来限制次数。
```python
# OutPut
over-and-over
over-and-over
over-and-over
over-and-over
over-and-over
```

当需要将某个固定值包含在其他迭代器的值中时，使用 `repeat()` 与 `zip()` 或 `map()` 组合会很有用。
```python
from itertools import repeat, count

for i, s in zip(count(), repeat('over-and-over', 5)):
    print(i, s)
```
在本例中，count值与 `repeat()` 返回的常量组合在一起。

此示例使用 `map()` 将从0到4的数字乘以2。
```python
from itertools import repeat

for i in map(lambda x, y: (x, y, x * y), repeat(2), range(5)):
    print('{:d} * {:d} = {:d}'.format(*i))
```

本例中 `repeat()` 不需要显式限制迭代次数，因为 `range()` 只返回五个元素, `map()` 在其任意输入结束时会停止处理。

```python
# OutPut
2 * 0 = 0
2 * 1 = 2
2 * 2 = 4
2 * 3 = 6
2 * 4 = 8
```


### 4.过滤

`dropwhile()` 函数的作用是:返回一个迭代器，直到条件第一次为false时，该迭代器开始才产生输入迭代器的元素。
```python
from itertools import dropwhile

def should_drop(x):
    print('输入:', x)
    return x < 1

for i in dropwhile(should_drop, [-1, 0, 1, 2, -2]):
    print('产出:', i)
```

`dropwhile()` 不会过滤每个输入项; 当第一次条件为假后，便直接返回输入中的所有剩余项目。
```python
# OutPut
输入: -1
输入: 0
输入: 1
产出: 1
产出: 2
产出: -2
```

与 `dropwhile()` 相反的是 `takewhile()` 。它返回一个迭代器，只要测试函数返回true, 该迭代器就返回输入迭代器中的项目。
```python
from itertools import takewhile

def should_take(x):
    print('输入:', x)
    return x < 1

for i in takewhile(should_take, [-1, 0, 1, 2, -2]):
    print('产生:', i)
```

一旦`should_take()`返回 `False`, `takewhile()`就停止处理输入。
```python
# OutPut
输入: -1
产生: -1
输入: 0
产生: 0
输入: 1
```

Python内置函数 `filter()` 是返回一个包含测试函数返回true的所有项的迭代器。
```python
def check_item(x):
    print('输入:', x)
    return x < 1

for i in filter(check_item, [-1, 0, 1, 2, -2]):
    print('产出:', i)
```
`filter()` 不同于 `dropwhile()` 和 `takewhile()` 的是，`filter()` 每个项目在返回之前都代入测试函数。
```python
# OutPut
输入: -1
产出: -1
输入: 0
产出: 0
输入: 1
输入: 2
输入: -2
产出: -2
```

`filterfalse()` 返回一个迭代器，该迭代器只包含测试函数返回false的项。
```python
from itertools import filterfalse

def check_item(x):
    print('输入:', x)
    return x < 1

for i in filterfalse(check_item, [-1, 0, 1, 2, -2]):
    print('产出:', i)
```

测试函数 `check_item()` 和上例中的一样，但是返回的结果正好和 `filter()` 相反。
```python
# OutPut
输入: -1
输入: 0
输入: 1
产出: 1
输入: 2
产出: 2
输入: -2
```

`compress()` 提供了另一种过滤可迭代内容的方法。它不再是调用函数，而是使用另一个迭代中的值来指示何时接受值何时忽略值。
```python
from itertools import compress, cycle

every_third = cycle([False, False, True])
data = range(1, 10)

for i in compress(data, every_third):
    print(i, end=' ')
```

`compress()` 的第一个参数是需要进行处理的可迭代数据，第二个参数是可迭代的生成的布尔值选择器，指示从数据输入中取出哪些元素（True产生值，False忽略）。
```python
# OutPut
3 6 9
```

### 5.聚合

`groupby()` 函数返回一个迭代器，该迭代器生成由公共键聚合的值集。下面例子展示基于属性对相关值进行分组。
```python
from itertools import groupby
import functools
import operator
import pprint


@functools.total_ordering
class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)


# 生成Point实例的数据集
data = list(map(Point, [1, 2, 3, 1, 2], range(5)))
print('Data:')
pprint.pprint(data, width=35)
print()

# 对无序的data基于属性x聚合
print('聚合, 无序data:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
print()

# 对data排序
data.sort()
print('排序后:')
pprint.pprint(data, width=35)
print()

# 对排序后的data基于属性X聚合
print('聚合, 有序data:')
for k, g in groupby(data, operator.attrgetter('x')):
    print(k, list(g))
```

输入序列需要根据键值进行排序处理后才输出预期的聚合结果。
```python
# OutPut
Data:
[(1, 0),
 (2, 1),
 (3, 2),
 (1, 3),
 (2, 4)]

聚合, 无序data:
1 [(1, 0)]
2 [(2, 1)]
3 [(3, 2)]
1 [(1, 3)]
2 [(2, 4)]

排序后:
[(1, 0),
 (1, 3),
 (2, 1),
 (2, 4),
 (3, 2)]

聚合, 有序data:
1 [(1, 0), (1, 3)]
2 [(2, 1), (2, 4)]
3 [(3, 2)]
```

### 6.组合

`accumulate()` 函数的作用是:处理可迭代的输入，将第n和n+1项传递给目标函数，生成返回值，而不是直接返回输入。默认函数功能是将两个值相加，因此可以使用 `accumulate()` 来生成一系列数值输入的累积和。
```python
from itertools import accumulate

print(list(accumulate(range(5))))
print(list(accumulate('abcde')))
```

如果输入序列是非整数值时，结果取决于将两个项“相加”在一起的含义。比如上面例子中的第二项 `accumulate()` 接收的是一个字符串，返回则是将字符串逐个拼接在一起。
```python
# OutPut
[0, 1, 3, 6, 10]
['a', 'ab', 'abc', 'abcd', 'abcde']
```

同时 `accumulate()` 也接受自定义的带有两个输入项的函数。
```python
from itertools import accumulate

def f(a, b):
    print(a, b)
    return b + a

print(list(accumulate('abcde', f)))
```

```python
# OutPut
a b
ba c
cba d
dcba e
['a', 'ba', 'cba', 'dcba', 'edcba']
```

如果嵌套for循环遍历多个序列可以使用 `product()` ，它会生成一个迭代器，其值是该组输入值的笛卡尔乘积。
```python
from itertools import product

char = ['a', 'b', 'c']
integer = [1, 2, 3]

for each in product(char, integer):
    print(each)
```

由 `product()` 产生的值是元组，由每个迭代中取出的成员按照它们传递的顺序作为参数传入。
```python
# OutPut
('a', 1)
('a', 2)
('a', 3)
('b', 1)
('b', 2)
('b', 3)
('c', 1)
('c', 2)
('c', 3)
```

如果要计算序列与其本身的笛卡尔积，则需要指定 `repeat` 参数。
```python
from itertools import product

char = ['a', 'b']

for each in product(char, repeat=2):
    print(each)

for each in product(char, repeat=2):
    print(each)
```

```python
# OutPut
('a', 'a', 'a')
('a', 'a', 'b')
('a', 'b', 'a')
('a', 'b', 'b')
('b', 'a', 'a')
('b', 'a', 'b')
('b', 'b', 'a')
('b', 'b', 'b')
```

`permutation()` 函数从输入的迭代的组合中生成指定长度的排列。它默认生成所有排列的完整集合。
```python
from itertools import permutations

for each in permutations('abc'):
    print(each)
print()

for each in permutations('abc', r=2):
    print(each)
```

使用 `r` 参数来限制返回的单个排列的长度。
```python
# OutPut
('a', 'b', 'c')
('a', 'c', 'b')
('b', 'a', 'c')
('b', 'c', 'a')
('c', 'a', 'b')
('c', 'b', 'a')

('a', 'b')
('a', 'c')
('b', 'a')
('b', 'c')
('c', 'a')
('c', 'b')
```

如果输出要保证唯一, 即需要组合而不是排列，请使用 `combination()` 。只要输入的成员是唯一的，输出就不会包含任何重复的值。
```python
from itertools import combinations

for each in combinations('abc', r=2):
    print(each)
```

与 `permutations()` 不同的是, `combination()` 必须传入 `r` 参数。
```python
# OutPut
('a', 'b')
('a', 'c')
('b', 'c')
```

因为 `combination()` 不重复单个输入元素，但考虑有时需要包含重复元素的组合。对于这些情况，可以使用 `combinations_with_replacement()` 。
```python
from itertools import combinations_with_replacement

for each in combinations_with_replacement('abc', r=2):
    print(each)
```

在此输出中，每个输入项都与其自身以及输入序列的所有其他成员组合。
```python
('a', 'a')
('a', 'b')
('a', 'c')
('b', 'b')
('b', 'c')
('c', 'c')

```
