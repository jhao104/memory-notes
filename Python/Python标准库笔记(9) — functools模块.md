> functools 作用于函数的函数

`functools` 模块提供用于调整或扩展函数和其他可调用对象的工具，而无需完全重写它们。

### 装饰器

`partial` 类是 `functools` 模块提供的主要工具, 它可以用来“包装”一个可调用的对象的默认参数。它产生的对象本身是可调用的，可以看作是原生函数。它所有的参数都与原来的相同，并且可以使用额外的位置参数或命名参数来调用。使用 `partial` 代替 `lambda` 来为函数提供默认参数，同时保留那些未指定的参数。

#### Partial 对象

下面列子是对 `myfunc` 方法的两个 `partial` 对象，`show_details()` 用于输出partial对象的 `func` 、 `args` 和 `keywords` 属性：

```python
import functools


def myfunc(a, b=2):
    """Docstring for myfunc()."""
    print('  传入参数:', (a, b))


def show_details(name, f, is_partial=False):
    """Show details of a callable object."""
    print('{}:'.format(name))
    print('  object:', f)
    if not is_partial:
        print('  __name__:', f.__name__)
    if is_partial:
        print('  func:', f.func)
        print('  args:', f.args)
        print('  keywords:', f.keywords)
    return


show_details('myfunc', myfunc)
myfunc('a', 3)
print()

# # 给'b'重新设置一个不同的默认参数
# # 调用时仍需提供参数'a'
p1 = functools.partial(myfunc, b=4)
show_details('partial 修改关键字参数', p1, True)
p1('传入 a')
p1('重写 b', b=5)
print()
#
# # 给 'a' 和 'b' 都设置默认参数.
p2 = functools.partial(myfunc, '默认 a', b=99)
show_details('partial 设置默认参数', p2, True)
p2()
p2(b='重写 b')
print()

print('参数缺失时:')
p1()
```

示例中最后调用第一个 `partial` 对象而没有传递 `a` 的值，导致异常。

```python
myfunc:
  object: <function myfunc at 0x00000180005077B8>
  __name__: myfunc
  传入参数: ('a', 3)

partial 修改关键字参数:
  object: functools.partial(<function myfunc at 0x00000180005077B8>, b=4)
  func: <function myfunc at 0x00000180005077B8>
  args: ()
  keywords: {'b': 4}
  传入参数: ('传入 a', 4)
  传入参数: ('重写 b', 5)

partial 设置默认参数:
  object: functools.partial(<function myfunc at 0x00000180005077B8>, '默认 a', b=99)
  func: <function myfunc at 0x00000180005077B8>
  args: ('默认 a',)
  keywords: {'b': 99}
  传入参数: ('默认 a', 99)
  传入参数: ('默认 a', '重写 b')

参数缺失时:
Traceback (most recent call last):
  File "functools_partial.py", line 51, in <module>
    p1()
TypeError: myfunc() missing 1 required positional argument: 'a'
```

#### 获取函数属性

默认情况下, `partial` 对象没有 `__name__` 和 `__doc__` 属性。 这样不利于被装饰的函数进行调试。可以使用 `update_wrapper()` 从原函数复制或新增属性到 `partial` 对象。

```python
import functools


def myfunc(a, b=2):
    """Docstring for myfunc()."""
    print('  传入参数:', (a, b))


def show_details(name, f):
    """Show details of a callable object."""
    print('{}:'.format(name))
    print('  object:', f)
    print('  __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
    print('  __doc__', repr(f.__doc__))
    print()


show_details('myfunc', myfunc)

p1 = functools.partial(myfunc, b=4)
show_details('raw wrapper', p1)

print('Updating wrapper:')
print('  assign:', functools.WRAPPER_ASSIGNMENTS)
print('  update:', functools.WRAPPER_UPDATES)
print()

functools.update_wrapper(p1, myfunc)
show_details('updated wrapper', p1)
```

添加到装饰器的属性在 `WRAPPER_ASSIGNMENTS` 中定义，而 `WRAPPER_UPDATES` 列出要修改的值。

```python
myfunc:
  object: <function myfunc at 0x000002315C123E18>
  __name__: myfunc
  __doc__ 'Docstring for myfunc().'

raw wrapper:
  object: functools.partial(<function myfunc at 0x000002315C123E18>, b=4)
  __name__: (no __name__)
  __doc__ 'partial(func, *args, **keywords) - new function with partial application\n    of the given arguments and keywords.\n'

Updating wrapper:
  assign: ('__module__', '__name__', '__qualname__', '__doc__', '__annotations__')
  update: ('__dict__',)

updated wrapper:
  object: functools.partial(<function myfunc at 0x000002315C123E18>, b=4)
  __name__: myfunc
  __doc__ 'Docstring for myfunc().'
```

#### 其他调用对象

partial适用于所有可调用可对象，并不是仅可用于独立函数。

```python
import functools


class MyClass:
    """Demonstration class for functools"""

    def __call__(self, e, f=6):
        "Docstring for MyClass.__call__"
        print('  called object with:', (self, e, f))


def show_details(name, f):
    """"Show details of a callable object."""
    print('{}:'.format(name))
    print('  object:', f)
    print('  __name__:', end=' ')
    try:
        print(f.__name__)
    except AttributeError:
        print('(no __name__)')
    print('  __doc__', repr(f.__doc__))
    return


o = MyClass()

show_details('instance', o)
o('e goes here')
print()

p = functools.partial(o, e='default for e', f=8)
functools.update_wrapper(p, o)
show_details('instance wrapper', p)
p()
```

上面例子使用 `MyClass` 类的实例的 `__call__()` 方法创建了partial对象。照样正常工作:

```python
instance:
  object: <__main__.MyClass object at 0x000002DE7C2CD2E8>
  __name__: (no __name__)
  __doc__ 'Demonstration class for functools'
  called object with: (<__main__.MyClass object at 0x000002DE7C2CD2E8>, 'e goes here', 6)

instance wrapper:
  object: functools.partial(<__main__.MyClass object at 0x000002DE7C2CD2E8>, e='default for e', f=8)
  __name__: (no __name__)
  __doc__ 'Demonstration class for functools'
  called object with: (<__main__.MyClass object at 0x000002DE7C2CD2E8>, 'default for e', 8)
```

#### 方法和函数

`partial()` 返回一个可以直接调用的对象， `partialmethod()` 返回一个可调用的为某个对象准备的未绑定的方法。再下面例子中，同一个独立函数被两次添加到类 `MyClass` 属性。使用 `partialmethod()` 生成 `method1（）`, `partial()` 生成 `method2()`:

```python
import functools


def standalone(self, a=1, b=2):
    """独立函数"""
    print('  called standalone with:', (self, a, b))
    if self is not None:
        print('  self.attr =', self.attr)


class MyClass:
    """"functools 示例类"""

    def __init__(self):
        self.attr = 'instance attribute'

    method1 = functools.partialmethod(standalone)
    method2 = functools.partial(standalone)


o = MyClass()

print('standalone')
standalone(None)
print()

print('method1 as partialmethod')
o.method1()
print()

print('method2 as partial')
try:
    o.method2()
except TypeError as err:
    print('ERROR: {}'.format(err))
```

`method1()` 可以被 `MyClass` 实例调用，和普通类方法一样，实例作为第一个参数传入。`method2()` 没有被成功绑定为类方法。因此其 `self` 参数必须显式传入，所以此例抛出 `TypeError` 异常:

```python
standalone
  called standalone with: (None, 1, 2)

method1 as partialmethod
  called standalone with: (<__main__.MyClass object at 0x00000214B4459B70>, 1, 2)
  self.attr = instance attribute

method2 as partial
ERROR: standalone() missing 1 required positional argument: 'self'
```

#### 在装饰器中使用

使用装饰器时保持函数的属性信息有时非常有用。但是使用装饰器时难免会损失一些原本的功能信息。所以functools提供了 `wraps()` 装饰器可以通过 `update_wrapper()` 将原函数对象的指定属性复制给包装函数对象。

```python
from functools import wraps

def logged1(func):
    def with_login(*args, **kwargs):
        print(func.__name__ + "was called")
        return func(*args, **kwargs)

    return with_login

@logged1
def f1(x):
    """ function doc"""
  return x + x * 1

def logged2(func):
    @wraps(func)
    def with_login(*args, **kwargs):
        print(func.__name__ + "was called")
        return func(*args, **kwargs)

    return with_login

@logged2
def f2(x):
    """ function doc """
  return x + x * 1

print("不使用functools.wraps时:")
print("__name__:  " + f1.__name__)
print("__doc__:  ", end=" ")
print(f1.__doc__)
print()

print("使用functools.wraps时:")
print("__name__:  " + f2.__name__)
print("__doc__:  ", end=" ")
print(f2.__doc__)
```

```python
不使用functools.wraps时:
__name__:  with_login
__doc__:   None

使用functools.wraps时:
__name__:  f2
__doc__:    function doc 
```

### 比较

在Python2之前,类中可以定义 `__cmp__()` 方法，该方法根据对象是否小于、d等于或大于被比较项返回-1、0或1。Python2.1开始引入了 *富比较* 方法API(`__lt__()`, `__le()__`, `__eq__()`, `__ne__()`, `__gt__()` 和 `__ge__()`)，用于执行比较操作返回一个布尔值。Python3中 ``__cmp__()`` 放弃支持这些新方法，由 `functools` 提供工具，以便于编写符合Python3中新的比较需求的类。

#### 富比较

富比较API旨在允许具有复杂比较的类以最有效的方式实现每种计算。但是，对于比较相对简单的类，手动创建每种富比较方法没有意义。`total_ordering()` 类装饰器可以使被装饰的类只需要定义 `__lt__()`,`__le__()`.`__gt__()`和`__ge__()` 中的其中一个和 `__eq__()`, 剩下的由该装饰器自动提供。这简化了定义所有富比较操作的工作量。

```python
import functools
import inspect
from pprint import pprint


@functools.total_ordering
class MyObject:

    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        print('  testing __eq__({}, {})'.format(
            self.val, other.val))
        return self.val == other.val

    def __gt__(self, other):
        print('  testing __gt__({}, {})'.format(
            self.val, other.val))
        return self.val > other.val


print("MyObject's Methods:\n")
pprint(inspect.getmembers(MyObject, inspect.isfunction))

a = MyObject(1)
b = MyObject(2)

print('\nComparisons:')
for expr in ['a < b', 'a <= b', 'a == b', 'a >= b', 'a > b']:
    print('\n{:<6}:'.format(expr))
    result = eval(expr)
    print('  result of {}: {}'.format(expr, result))
```

```python
MyObject's Methods:

[('__eq__', <function MyObject.__eq__ at 0x0000021DE4DB4048>),
 ('__ge__', <function _ge_from_gt at 0x0000021DDDE5D268>),
 ('__gt__', <function MyObject.__gt__ at 0x0000021DE4DB40D0>),
 ('__init__', <function MyObject.__init__ at 0x0000021DDDE877B8>),
 ('__le__', <function _le_from_gt at 0x0000021DDDE5D2F0>),
 ('__lt__', <function _lt_from_gt at 0x0000021DDDE5D1E0>)]

Comparisons:

a < b :
  testing __gt__(1, 2)
  testing __eq__(1, 2)
  result of a < b: True

a <= b:
  testing __gt__(1, 2)
  result of a <= b: True

a == b:
  testing __eq__(1, 2)
  result of a == b: False

a >= b:
  testing __gt__(1, 2)
  testing __eq__(1, 2)
  result of a >= b: False

a > b :
  testing __gt__(1, 2)
  result of a > b: False
```

虽然该装饰器能很容易的创建完全有序类型，但衍生出的比较函数执行的可能会更慢，以及产生更复杂的堆栈跟踪。如果性能基准测试表明这是程序的瓶颈，则实现所有六个富比较函数可能会提高速度。

#### 排序规则

在Python3中已经废弃了旧时的比较(cmp)函数，因此例如 `sorted()`,`min()`,`max()`等方法不在支持 `cmp`参数， 但仍然支持key函数。functools提供了 `cmp_to_key()` 用于将cmp函数转换成key函数。

例如给定一个正整数列表，输出用这些正整数能够拼接成的最大整数。如果是Python2的程序可以是这样:

```python
L = [97, 13, 4, 246]

def my_cmp(a, b):
    """ 将比较的两个数字拼接成整数, 比较数值大小"""
    return int(str(b) + str(a)) - int(str(a) + str(b))

L.sort(cmp=my_cmp)
print(''.join(map(str, L)))

# 输出 97424613
```

但Python3的 `sort` 函数已废弃 `cmp` 参数，可以使用 `cmp_to_key` 将cmp函数转换成key函数:

```python
from functools import cmp_to_key

L = [97, 13, 4, 246]


def my_cmp(a, b):
    """ 将比较的两个数字拼接成整数, 比较数值大小"""
    return int(str(b) + str(a)) - int(str(a) + str(b))


L.sort(key=cmp_to_key(my_cmp))
print(''.join(map(str, L)))

# 输出 97424613
```

`cmp` 函数接收两个参数，比较它们，如果小于返回负数，相等返回0，大于返回正数。 `key` 函数接收一个参数，返回用于排序的键。

### 缓存

`lru_cache()` 装饰器是 *缓存淘汰算法*(最近最少使用)的一种实现。其使用函数的参数作为key结果作为value缓存在hash结构中(因此函数的参数必须是hashable)，如果后续使用相同参数再次调用将从hash从返回结果。同时装饰器还添加了检查缓存转态方法(`cache_info()`)和清空缓存方法(`cache_clear()`)给函数。

```python
import functools


@functools.lru_cache()
def demo(a):
    print('called demo with {}'.format(a))
    return a ^ 2


MAX = 2

print('初次调用:')
for i in range(MAX):
    demo(i)
print(demo.cache_info())

print('\n第二次调用:')
for i in range(MAX + 1):
    demo(i)
print(demo.cache_info())

print('\n清空缓存后:')
demo.cache_clear()
print(demo.cache_info())

print('\n再次调用:')
for i in range(MAX):
    demo(i)
print(demo.cache_info())
```

代码中多次调用 `demo()` 方法。首次调用后结果存在缓存中。`cache_info()` 返回一个命名元组，包括 `hits`,`misses`,`maxsize` 和 `currsize` 。当第二次调用时命中缓存的调用将直接返回缓存内容，`cache_clear()` 用于清空当前缓存。

```python
初次调用:
called demo with 0
called demo with 1
CacheInfo(hits=0, misses=2, maxsize=128, currsize=2)

第二次调用:
called demo with 2
CacheInfo(hits=2, misses=3, maxsize=128, currsize=3)

清空缓存后:
CacheInfo(hits=0, misses=0, maxsize=128, currsize=0)

再次调用:
called demo with 0
called demo with 1
CacheInfo(hits=0, misses=2, maxsize=128, currsize=2)
```

为了防止缓存在长时间运行的流程中无限制地增长，特别设置了 `maxsize` 参数, 默认是128，设置为None时，则禁用LRU功能,缓存可以无限增长。同时还提供了 `typed` 参数，用于设置是否区别参数类型，默认为Fals。如果设置为True，那么类似如 `demo(1)` 和 `demo(1.0)` 将被视为不同的值不同的调用。

### Reduce方法

Python3中取消了全局命名空间中的 `reduce()` 函数，将 `reduced()` 放到了 `functools` 模块中，要使用 `reduce()` 的话，要先从 `functools` 中加载。

```python
from functools import reduce

print(reduce(lambda a, b: a + b, range(11)))

# 计算1加到10 结果 55

```

### 函数重载

在动态类型的语言(如Python)中，如果需要根据参数的类型执行不同的操作，简单直接的方法就是检查参数的类型。但在行为差异明显的情况下需要分离成单独的函数。 `functools` 提供 `singledispatch()` 装饰器注册一组通用函数基于函数的第一个参数的类型自动切换,类似于强类型语言中的函数重载。

```python
import functools


@functools.singledispatch
def myfunc(arg):
    print('default myfunc({!r})'.format(arg))


@myfunc.register(int)
def myfunc_int(arg):
    print('myfunc_int({})'.format(arg))


@myfunc.register(list)
def myfunc_list(arg):
    print('myfunc_list({})'.format(' '.join(arg)))


myfunc('string argument')
myfunc(1)
myfunc(2.3)
myfunc(['a', 'b', 'c'])
```

被 `singledispatch()` 装饰的函数是默认实现， 使用其 `register()` 属性装饰接收其他类型参数的函数。调用时会根据 `register()` 中注册的类型自动选择实现函数。没有则使用默认实现。

```python
default myfunc('string argument')
myfunc_int(1)
default myfunc(2.3)
myfunc_list(a b c)
```

另外再有继承的情况下，当类型没有精确匹配时，将根据继承顺序，选择最接近的类型。

```python
import functools


class A:
    pass


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(C, D):
    pass


@functools.singledispatch
def myfunc(arg):
    print('default myfunc({})'.format(arg.__class__.__name__))


@myfunc.register(A)
def myfunc_A(arg):
    print('myfunc_A({})'.format(arg.__class__.__name__))


@myfunc.register(B)
def myfunc_B(arg):
    print('myfunc_B({})'.format(arg.__class__.__name__))


@myfunc.register(C)
def myfunc_C(arg):
    print('myfunc_C({})'.format(arg.__class__.__name__))


myfunc(A())
myfunc(B())
myfunc(C())
myfunc(D())
myfunc(E())
```

```python
myfunc_A(A)
myfunc_B(B)
myfunc_C(C)
myfunc_B(D)
myfunc_C(E)
```

在上面代码中，类D和E没有与任何已注册的泛型函数匹配，所以根据其类的继承顺序进行选择。




