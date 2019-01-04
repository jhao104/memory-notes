> Operator——标准功能性操作符接口.

代码中使用迭代器时,有时必须要为一个简单表达式创建函数。有些情况这些函数可以用一个`lambda`函数实现，但是对于某些操作，根本没必要去写一个新的函数。因此`operator`模块定义了一些函数，这些函数对应于算术、比较和其他与标准对象API对应的操作。

### 1.逻辑操作符(Logical Operations)

下面函数用于确定一个值的布尔等价值，或者否定它创建相反的布尔值，或比较对象确定它们是否相同。

```python
from operator import *

a = -1
b = 5

print('a =', a)
print('b =', b)
print()

print('not_(a)     :', not_(a))
print('truth(a)    :', truth(a))
print('is_(a, b)   :', is_(a, b))
print('is_not(a, b):', is_not(a, b))
```

`not_()`后面有一个下划线，是因为`not`是Python关键字。`true()`使用的逻辑和`if`语句加表达式或将表达式转换为`bool.is_()`时相同的逻辑。`is_()`实现的是使用`is`关键字相同的检查，`is_not()`也执行相同的检查但返回相反的结果。

```python
a = -1
b = 5

not_(a)     : False
truth(a)    : True
is_(a, b)   : False
is_not(a, b): True
```

### 2.比较操作符(Comparison Operators)

它支持所有富比较操作符：

```python
from operator import *

a = 1
b = 5.0

print('a =', a)
print('b =', b)

for func in (lt, le, eq, ne, ge, gt):
    print('{}(a, b): {}'.format(func.__name__, func(a, b)))
```

这些函数等价于使用`<`、`<=`、`==`、`>=`和`>`的表达式语法。

```python
a = 1
b = 5.0
lt(a, b): True
le(a, b): True
eq(a, b): False
ne(a, b): True
ge(a, b): False
gt(a, b): False
```

### 3.算术操作符(Arithmetic Operators)

它还支持用于操作数值的算术运算符：

```python
from operator import *

a = -1
b = 5.0
c = 2
d = 6

print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)

print('\n正数/负数:')
print('abs(a):', abs(a))
print('neg(a):', neg(a))
print('neg(b):', neg(b))
print('pos(a):', pos(a))
print('pos(b):', pos(b))

print('\n算术:')
print('add(a, b)     :', add(a, b))
print('floordiv(a, b):', floordiv(a, b))
print('floordiv(d, c):', floordiv(d, c))
print('mod(a, b)     :', mod(a, b))
print('mul(a, b)     :', mul(a, b))
print('pow(c, d)     :', pow(c, d))
print('sub(b, a)     :', sub(b, a))
print('truediv(a, b) :', truediv(a, b))
print('truediv(d, c) :', truediv(d, c))

print('\n按位:')
print('and_(c, d)  :', and_(c, d))
print('invert(c)   :', invert(c))
print('lshift(c, d):', lshift(c, d))
print('or_(c, d)   :', or_(c, d))
print('rshift(d, c):', rshift(d, c))
print('xor(c, d)   :', xor(c, d))
```

有两种除法运算符:`floordiv()`(在3.0版本之前Python中实现的整数除法)和`truediv()`(浮点除法)。

```python
a = -1
b = 5.0
c = 2
d = 6

正数/负数:
abs(a): 1
neg(a): 1
neg(b): -5.0
pos(a): -1
pos(b): 5.0

算术:
add(a, b)     : 4.0
floordiv(a, b): -1.0
floordiv(d, c): 3
mod(a, b)     : 4.0
mul(a, b)     : -5.0
pow(c, d)     : 64
sub(b, a)     : 6.0
truediv(a, b) : -0.2
truediv(d, c) : 3.0

按位:
and_(c, d)  : 2
invert(c)   : -3
lshift(c, d): 128
or_(c, d)   : 6
rshift(d, c): 1
xor(c, d)   : 4
```

### 4.序列操作符(Sequence Operators)

处理序列的操作符可以分为四种:构建序列、搜索条目、访问内容和从序列中删除条目:

```python
from operator import *

a = [1, 2, 3]
b = ['a', 'b', 'c']

print('a =', a)
print('b =', b)

print('\n构建序列:')
print('  concat(a, b):', concat(a, b))

print('\n搜索:')
print('  contains(a, 1)  :', contains(a, 1))
print('  contains(b, "d"):', contains(b, "d"))
print('  countOf(a, 1)   :', countOf(a, 1))
print('  countOf(b, "d") :', countOf(b, "d"))
print('  indexOf(a, 5)   :', indexOf(a, 1))

print('\n访问:')
print('  getitem(b, 1)                  :',
      getitem(b, 1))
print('  getitem(b, slice(1, 3))        :',
      getitem(b, slice(1, 3)))
print('  setitem(b, 1, "d")             :', end=' ')
setitem(b, 1, "d")
print(b)
print('  setitem(a, slice(1, 3), [4, 5]):', end=' ')
setitem(a, slice(1, 3), [4, 5])
print(a)

print('\n删除:')
print('  delitem(b, 1)          :', end=' ')
delitem(b, 1)
print(b)
print('  delitem(a, slice(1, 3)):', end=' ')
delitem(a, slice(1, 3))
print(a)

```

其中一些操作，如`setitem()`和`delitem()`，修改序列时属于原地操作，不返回值。

```python
a = [1, 2, 3]
b = ['a', 'b', 'c']

构建序列:
  concat(a, b): [1, 2, 3, 'a', 'b', 'c']

搜索:
  contains(a, 1)  : True
  contains(b, "d"): False
  countOf(a, 1)   : 1
  countOf(b, "d") : 0
  indexOf(a, 5)   : 0

访问:
  getitem(b, 1)                  : b
  getitem(b, slice(1, 3))        : ['b', 'c']
  setitem(b, 1, "d")             : ['a', 'd', 'c']
  setitem(a, slice(1, 3), [4, 5]): [1, 4, 5]

删除:
  delitem(b, 1)          : ['a', 'c']
  delitem(a, slice(1, 3)): [1]
```

### 5.原地操作符(In-place Operators)

除了标准操作符之外，许多对象类型还支持通过特殊操作符(如`+=`)"原地"修改。原地操作符也有相同的功能:

```python
from operator import *

a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']
print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)
print()

iadd(a, b)
print('a = iadd(a, b) =>', a)
print()

iconcat(c, d)
print('c = iconcat(c, d) =>', c)
```

上面示例只演示了个别函数。有关详细信息，请参阅[标准库文档](https://docs.python.org/3/library/operator.html#inplace-operators)。

```python
a = -1
b = 5.0
c = [1, 2, 3]
d = ['a', 'b', 'c']

a = iadd(a, b) => -1

c = iconcat(c, d) => [1, 2, 3, 'a', 'b', 'c']
```

### 6.属性和内容"Getters"

operator模块最出众的特性之一就是`getter`的概念。这些是在运行时构造的可调用对象，用于从序列中检索对象属性或内容。`getter`在处理迭代器或生成器序列时特别有用，因为它们的开销要小于`lambda`和Python函数。

```python
from operator import *


class MyObj:
    """attrgetter 演示类"""

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def __repr__(self):
        return 'MyObj({})'.format(self.arg)


l = [MyObj(i) for i in range(5)]
print('objects   :', l)

# 从每个对象中提取'arg'属性
g = attrgetter('arg')
vals = [g(i) for i in l]
print('arg values:', vals)

# 使用arg排序
l.reverse()
print('reversed  :', l)
print('sorted    :', sorted(l, key=g))
```

本例中的属性getters功能类似于:`lambda x, n='attrname': getattr(x, n)`:

```python
objects   : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]
arg values: [0, 1, 2, 3, 4]
reversed  : [MyObj(4), MyObj(3), MyObj(2), MyObj(1), MyObj(0)]
sorted    : [MyObj(0), MyObj(1), MyObj(2), MyObj(3), MyObj(4)]

```

而内容getters功能类似于`lambda x, y=5: x[y]`:

```python
from operator import *

l = [dict(val=-1 * i) for i in range(4)]
print('Dictionaries:')
print(' original:', l)
g = itemgetter('val')
vals = [g(i) for i in l]
print('   values:', vals)
print('   sorted:', sorted(l, key=g))

print()
l = [(i, i * -2) for i in range(4)]
print('\nTuples:')
print(' original:', l)
g = itemgetter(1)
vals = [g(i) for i in l]
print('   values:', vals)
print('   sorted:', sorted(l, key=g))
```

内容getters既可以处字典，也可以处理序列。

```python
Dictionaries:
 original: [{'val': 0}, {'val': -1}, {'val': -2}, {'val': -3}]
   values: [0, -1, -2, -3]
   sorted: [{'val': -3}, {'val': -2}, {'val': -1}, {'val': 0}]


Tuples:
 original: [(0, 0), (1, -2), (2, -4), (3, -6)]
   values: [0, -2, -4, -6]
   sorted: [(3, -6), (2, -4), (1, -2), (0, 0)]
```

### 7.自定义类中使用

operator模块中的函数操作是通过标准的Python接口工作，因此它们也可以处理用户自定义的类和内置类型。

```python
from operator import *


class MyObj:
    """重载操作符例子"""

    def __init__(self, val):
        super(MyObj, self).__init__()
        self.val = val

    def __str__(self):
        return 'MyObj({})'.format(self.val)

    def __lt__(self, other):
        """小于比较"""
        print('Testing {} < {}'.format(self, other))
        return self.val < other.val

    def __add__(self, other):
        """add操作"""
        print('Adding {} + {}'.format(self, other))
        return MyObj(self.val + other.val)


a = MyObj(1)
b = MyObj(2)

print('比较操作:')
print(lt(a, b))

print('\n算术运算:')
print(add(a, b))
```

```python
比较操作:
Testing MyObj(1) < MyObj(2)
True

算术运算:
Adding MyObj(1) + MyObj(2)
MyObj(3)
```