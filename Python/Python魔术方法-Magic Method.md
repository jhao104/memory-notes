## 介绍

　　在Python中，所有以“__”双下划线包起来的方法，都统称为“Magic Method”,例如类的初始化方法 *\__init__* ,Python中所有的魔术方法均在官方文档中有相应描述，但是对于官方的描述比较混乱而且组织比较松散。很难找到有一个例子。

## 构造和初始化

　　每个Pythoner都知道一个最基本的魔术方法， *\__init__* 。通过此方法我们可以定义一个对象的初始操作。然而，当调用 x = SomeClass() 的时候， *\__init__* 并不是第一个被调用的方法。实际上，还有一个叫做*\__new__* 的方法，两个共同构成了“构造函数”。

　　*\__new__*是用来创建类并返回这个类的实例, 而*\__init__*只是将传入的参数来初始化该实例。

　　在对象生命周期调用结束时，*\__del__* 方法会被调用，可以将*\__del__*理解为“构析函数”。下面通过代码的看一看这三个方法:

```
from os.path import join

class FileObject:
    '''给文件对象进行包装从而确认在删除时文件流关闭'''

    def __init__(self, filepath='~', filename='sample.txt'):
        #读写模式打开一个文件
        self.file = open(join(filepath, filename), 'r+')

    def __del__(self):
        self.file.close()
        del self.file
```

## 控制属性访问

　　许多从其他语言转到Python的人会抱怨它缺乏类的真正封装。(没有办法定义私有变量，然后定义公共的getter和setter)。Python其实可以通过魔术方法来完成封装。我们来看一下:

* *\__getattr__(self, name)*:

　　定义当用户试图获取一个不存在的属性时的行为。这适用于对普通拼写错误的获取和重定向，对获取一些不建议的属性时候给出警告(如果你愿意你也可以计算并且给出一个值)或者处理一个 *AttributeError* 。只有当调用不存在的属性的时候会被返回。

* *\__setattr__(self, name, value)*:

　　与*\__getattr__(self, name)*不同，*\__setattr__* 是一个封装的解决方案。无论属性是否存在，它都允许你定义对对属性的赋值行为，以为这你可以对属性的值进行个性定制。实现*\__setattr__*时要避免"无限递归"的错误。

* *\__delattr__*:

　　与 *\__setattr__* 相同，但是功能是删除一个属性而不是设置他们。实现时也要防止无限递归现象发生。

* *\__getattribute__(self, name)*:

　　*\__getattribute__*定义了你的属性被访问时的行为，相比较，*\__getattr__*只有该属性不存在时才会起作用。因此，在支持*\__getattribute__*的Python版本,调用*\__getattr__*前必定会调用 *\__getattribute__*。*\__getattribute__*同样要避免"无限递归"的错误。需要提醒的是，最好不要尝试去实现*\__getattribute__*,因为很少见到这种做法，而且很容易出bug。

　　在进行属性访问控制定义的时候很可能会很容易引起“无限递归”。如下面代码:

```
#  错误用法
def __setattr__(self, name, value):
    self.name = value
    # 每当属性被赋值的时候(如self.name = value)， ``__setattr__()`` 会被调用，这样就造成了递归调用。
    # 这意味这会调用 ``self.__setattr__('name', value)`` ，每次方法会调用自己。这样会造成程序崩溃。

#  正确用法
def __setattr__(self, name, value):
    self.__dict__[name] = value  # 给类中的属性名分配值
    # 定制特有属性
```

   Python的魔术方法很强大，但是用时却需要慎之又慎，了解正确的使用方法非常重要。

## 创建自定义容器

　　有很多方法可以让你的Python类行为向内置容器类型一样，比如我们常用的list、dict、tuple、string等等。Python的容器类型分为可变类型(如list、dict)和不可变类型（如string、tuple），可变容器和不可变容器的区别在于，不可变容器一旦赋值后，不可对其中的某个元素进行修改。
　　在讲创建自定义容器之前，应该先了解下协议。这里的协议跟其他语言中所谓的"接口"概念很像，它给你很多你必须定义的方法。然而在Python中的协议是很不正式的，不需要明确声明实现。事实上，他们更像一种指南。

### 自定义容器的magic method

　　下面细致了解下定义容器可能用到的魔术方法。首先，实现不可变容器的话，你只能定义 *\__len__* 和 *\__getitem__* (下面会讲更多)。可变容器协议则需要所有不可变容器的所有，另外还需要 *\__setitem__* 和 *\__delitem__* 。如果你希望你的对象是可迭代的话，你需要定义 *\__iter__* 会返回一个迭代器。迭代器必须遵循迭代器协议，需要有 *\__iter__ *(返回它本身) 和 next。

* *\__len__(self)*:

　　返回容器的长度。对于可变和不可变容器的协议，这都是其中的一部分。

* *\__getitem__(self, key)*:

　　定义当某一项被访问时，使用*self\[key]*所产生的行为。这也是不可变容器和可变容器协议的一部分。如果键的类型错误将产生TypeError；如果key没有合适的值则产生KeyError。

* *\__setitem__(self, key, value)*:

　　当你执行*self[key] = value*时，调用的是该方法。

* *\__delitem__(self, key)*:

　　定义当一个项目被删除时的行为(比如 *del self[key]*)。这只是可变容器协议中的一部分。当使用一个无效的键时应该抛出适当的异常。

* *\__iter__(self)*:

　　返回一个容器迭代器，很多情况下会返回迭代器，尤其是当内置的*iter()*方法被调用的时候，以及当使用*for x in container:*方式循环的时候。迭代器是它们本身的对象，它们必须定义返回*self*的*\__iter__*方法。

* *\__reversed__(self)*:

　　实现当*reversed()*被调用时的行为。应该返回序列反转后的版本。仅当序列可以是有序的时候实现它，例如对于列表或者元组。

* *\__contains__(self, item)*:

　　定义了调用in和not in来测试成员是否存在的时候所产生的行为。你可能会问为什么这个不是序列协议的一部分？因为当*\__contains__*没有被定义的时候，如果没有定义，那么Python会迭代容器中的元素来一个一个比较，从而决定返回True或者False。

* *\__missing__(self, key)*:

　　dict字典类型会有该方法，它定义了key如果在容器中找不到时触发的行为。比如*d = {'a': 1}*, 当你执行*d[notexist]*时，*d.\__missing__['notexist']*就会被调用。

### 一个列子

　　下面是书中的例子，用魔术方法来实现Haskell语言中的一个数据结构。
```
# -*- coding: utf-8 -*-
class FunctionalList:
    ''' 实现了内置类型list的功能,并丰富了一些其他方法: head, tail, init, last, drop, take'''

    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __delitem__(self, key):
        del self.values[key]

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return FunctionalList(reversed(self.values))

    def append(self, value):
        self.values.append(value)
    def head(self):
        # 获取第一个元素
        return self.values[0]
    def tail(self):
        # 获取第一个元素之后的所有元素
        return self.values[1:]
    def init(self):
        # 获取最后一个元素之前的所有元素
        return self.values[:-1]
    def last(self):
        # 获取最后一个元素
        return self.values[-1]
    def drop(self, n):
        # 获取所有元素，除了前N个
        return self.values[n:]
    def take(self, n):
        # 获取前N个元素
        return self.values[:n]
```
　　
　　其实在collections模块中已经有了很多类似的实现，比如Counter、OrderedDict等等。

## 反射

　　你也可以控制怎么使用内置在函数sisinstance()和issubclass()方法 反射定义魔术方法. 这个魔术方法是:

* *\__instancecheck__(self, instance)*:

　　检查一个实例是不是你定义的类的实例

* *\__subclasscheck__(self, subclass)*:
　　检查一个类是不是你定义的类的子类

　　这些魔术方法的用例看起来很小, 并且确实非常实用. 它们反应了关于面向对象程序上一些重要的东西在Python上,并且总的来说Python: 总是一个简单的方法去找某些事情, 即使是没有必要的. 这些魔法方法可能看起来不是很有用, 但是一旦你需要它们，你会感到庆幸它们的存在。

## 可调用的对象

　　你也许已经知道，在Python中，方法是最高级的对象。这意味着他们也可以被传递到方法中，就像其他对象一样。这是一个非常惊人的特性。

　　在Python中，一个特殊的魔术方法可以让类的实例的行为表现的像函数一样，你可以调用它们，将一个函数当做一个参数传到另外一个函数中等等。这是一个非常强大的特性，其让Python编程更加舒适甜美。

* *\__call__(self, [args...])*:

　　允许一个类的实例像函数一样被调用。实质上说，这意味着 *x()* 与 *x.\__call__()* 是相同的。注意 *\__call__* 的参数可变。这意味着你可以定义 *\__call__* 为其他你想要的函数，无论有多少个参数。

　　*\__call__* 在那些类的实例经常改变状态的时候会非常有效。调用这个实例是一种改变这个对象状态的直接和优雅的做法。用一个实例来表达最好不过了:
```
# -*- coding: UTF-8 -*-

class Entity:
    """
    调用实体来改变实体的位置
    """

def __init__(self, size, x, y):
    self.x, self.y = x, y
    self.size = size


def __call__(self, x, y):
    """
    改变实体的位置
    """
    self.x, self.y = x, y
```

## 上下文管理

　　*with*声明是从Python2.5开始引进的关键词。你应该遇过这样子的代码:
```
with open('foo.txt') as bar:
    # do something with bar
```

　　在with声明的代码段中，我们可以做一些对象的开始操作和退出操作,还能对异常进行处理。这需要实现两个魔术方法: *\__enter__* 和 *\__exit__*。

* *\__enter__(self)*:

　　定义了当使用with语句的时候，会话管理器在块被初始创建时要产生的行为。请注意，*\__enter__*的返回值与with语句的目标或者as后的名字绑定。

* *\__exit__(self, exception_type, exception_value, traceback)*:

　　定义了当一个代码块被执行或者终止后，会话管理器应该做什么。它可以被用来处理异常、执行清理工作或做一些代码块执行完毕之后的日常工作。如果代码块执行成功，exception_type，exception_value，和traceback将会为None。否则，你可以选择处理这个异常或者是直接交给用户处理。如果你想处理这个异常的话，请确保*\__exit__*在所有语句结束之后返回True。如果你想让异常被会话管理器处理的话，那么就让其产生该异常。

## 创建对象描述器

　　描述器是通过获取、设置以及删除的时候被访问的类。当然也可以改变其它的对象。描述器并不是独立的。相反，它意味着被一个所有者类持有。当创建面向对象的数据库或者类，里面含有相互依赖的属相时，描述器将会非常有用。一种典型的使用方法是用不同的单位表示同一个数值，或者表示某个数据的附加属性。
　　为了成为一个描述器，一个类必须至少有*\__get__*，*\__set__*，*\__delete__*方法被实现：

* *\__get__(self, instance, owner)*:

    定义了当描述器的值被取得的时候的行为。instance是拥有该描述器对象的一个实例。owner是拥有者本身
    
* *\__set__(self, instance, value)*:

    定义了当描述器的值被改变的时候的行为。instance是拥有该描述器类的一个实例。value是要设置的值。

* *\__delete__(self, instance)*:

    定义了当描述器的值被删除的时候的行为。instance是拥有该描述器对象的一个实例。

　　下面是一个描述器的实例：单位转换。
```
# -*- coding: UTF-8 -*-
class Meter(object):
    """
    对于单位"米"的描述器
    """

    def __init__(self, value=0.0):
        self.value = float(value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = float(value)


class Foot(object):
    """
    对于单位"英尺"的描述器
    """

    def __get__(self, instance, owner):
        return instance.meter * 3.2808

    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808


class Distance(object):
    """
    用米和英寸来表示两个描述器之间的距离
    """
    meter = Meter(10)
    foot = Foot()
```
　　使用时：
```
>>>d = Distance()
>>>print d.foot
>>>print d.meter
32.808
10.0
```

## 复制

　　有时候，尤其是当你在处理可变对象时，你可能想要复制一个对象，然后对其做出一些改变而不希望影响原来的对象。这就是Python的copy所发挥作用的地方。

* *\__copy__(self)*:

　　定义了当对你的类的实例调用*copy.copy()*时所产生的行为。*copy.copy()*返回了你的对象的一个浅拷贝——这意味着，当实例本身是一个新实例时，它的所有数据都被引用了——例如，当一个对象本身被复制了，它的数据仍然是被引用的（因此，对于浅拷贝中数据的更改仍然可能导致数据在原始对象的中的改变）。

* *\__deepcopy__(self, memodict={})*:

　　定义了当对你的类的实例调用*copy.deepcopy()*时所产生的行为。*copy.deepcopy()*返回了你的对象的一个深拷贝——对象和其数据都被拷贝了。memodict是对之前被拷贝的对象的一个缓存——这优化了拷贝过程并且阻止了对递归数据结构拷贝时的无限递归。当你想要进行对一个单独的属性进行深拷贝时，调用*copy.deepcopy()*，并以memodict为第一个参数。

## 附录

### 用于比较的魔术方法

| Magic method  | explain |
|---| --- |
|\__cmp__(self, other)   |__cmp__ 是比较方法里面最基本的的魔法方法|
|\__eq__(self, other)|定义相等符号的行为，==|
|\__ne__(self,other)|定义不等符号的行为，！=|
|\__lt__(self,other)|定义小于符号的行为，<|
|\__gt__(self,other)|定义大于符号的行为，>|
|\__le__(self,other)|定义小于等于符号的行为，<=|
|\__ge__(self,other)|定义大于等于符号的行为，>=|

### 数值计算的魔术方法

单目运算符和函数

| Magic method  | explain|
|---|---|
|\__pos__(self)   |实现一个取正数的操作|
|\__neg__(self)|实现一个取负数的操作|
|\__abs__(self)|实现一个内建的abs()函数的行为|
|__invert__(self)|实现一个取反操作符（～操作符）的行为|
|\__round__(self, n)|实现一个内建的round（）函数的行为|
|\__floor__(self)|实现math.floor()的函数行为|
|\__ceil__(self)|实现math.ceil()的函数行为|
|\__trunc__(self)|实现math.trunc()的函数行为|

双目运算符或函数

| Magic method  | explain|
|---|---|
|\__add__(self, other)   |实现一个加法|
|\__sub__(self, other)|实现一个减法|
|\__mul__(self, other)|实现一个乘法|
|\__floordiv__(self, other)|实现一个“//”操作符产生的整除操作（）|
|\__div__(self, other)|实现一个“/”操作符代表的除法操作|
|\__truediv__(self, other)|实现真实除法|
|\__mod__(self, other)|实现一个“%”操作符代表的取模操作|
|\__divmod__(self, other)|实现一个内建函数divmod（）|
|\__pow__|实现一个指数操作(“\*\*”操作符）的行为|
|\__lshift__(self, other)|实现一个位左移操作（<<）的功能|
|\__rshift__(self, other)|实现一个位右移操作（>>）的功能|
|\__and__(self, other)|实现一个按位进行与操作（&）的行为|
|\__or__(self, other) |实现一个按位进行或操作（\|）的行为|
|\__xor__(self, other)|__xor__(self, other)|


