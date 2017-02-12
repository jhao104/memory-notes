##单继承时super()和__init__()实现的功能是类似的
```python
class Base(object):
    def __init__(self):
        print 'Base create'

class childA(Base):
    def __init__(self):
        print 'creat A ',
        Base.__init__(self)


class childB(Base):
    def __init__(self):
        print 'creat B ',
        super(childB, self).__init__()

base = Base()

a = childA()
b = childB()
```

输出结果：
```
Base create
creat A  Base create
creat B  Base create
```

区别是使用super()继承时不用显式引用基类。


##super()只能用于新式类中

把基类改为旧式类，即不继承任何基类
```python
class Base():
    def __init__(self):
        print 'Base create'
```
执行时，在初始化b时就会报错：
```python
super(childB, self).__init__()
TypeError: must be type, not classobj
```


##super不是父类，而是继承顺序的下一个类
在多重继承时会涉及继承顺序，super（）相当于返回继承顺序的下一个类，而不是父类，类似于这样的功能：
```python
def super(class_name, self):
    mro = self.__class__.mro()
    return mro[mro.index(class_name) + 1]
```
mro()用来获得类的继承顺序。
例如：
```python
class Base(object):
    def __init__(self):
        print 'Base create'

class childA(Base):
    def __init__(self):
        print 'enter A '
        # Base.__init__(self)
        super(childA, self).__init__()
        print 'leave A'


class childB(Base):
    def __init__(self):
        print 'enter B '
        # Base.__init__(self)
        super(childB, self).__init__()
        print 'leave B'

class childC(childA, childB):
    pass

c = childC()
print c.__class__.__mro__
```
输出结果如下：
```
enter A 
enter B 
Base create
leave B
leave A
(<class '__main__.childC'>, <class '__main__.childA'>, <class '__main__.childB'>, <class '__main__.Base'>, <type 'object'>)
```
supder和父类没有关联，因此执行顺序是A —> B—>—>Base

执行过程相当于：初始化childC()时，先会去调用childA的构造方法中的 super(childA, self).\__init\__()， super(childA, self)返回当前类的继承顺序中childA后的一个类childB；然后再执行childB().\__init()\__,这样顺序执行下去。

在多重继承里，如果把childA()中的 super(childA, self).\__init\__() 换成Base.\__init\__(self)，在执行时，继承childA后就会直接跳到Base类里，而略过了childB：
```
enter A 
Base create
leave A
(<class '__main__.childC'>, <class '__main__.childA'>, <class '__main__.childB'>, <class '__main__.Base'>, <type 'object'>)
```
从super()方法可以看出，super（）的第一个参数可以是继承链中任意一个类的名字，

如果是本身就会依次继承下一个类；

如果是继承链里之前的类便会无限递归下去；

如果是继承链里之后的类便会忽略继承链汇总本身和传入类之间的类；

比如将childA()中的super改为：`super(childC, self).__init__()`，程序就会无限递归下去。
如：
```
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
  File "C:/Users/Administrator/Desktop/crawler/learn.py", line 10, in __init__
    super(childC, self).__init__()
RuntimeError: maximum recursion depth exceeded while calling a Python object
```


##super()可以避免重复调用
如果childA基础Base, childB继承childA和Base，如果childB需要调用Base的__init__()方法时，就会导致__init__()被执行两次：
```python
class Base(object):
    def __init__(self):
        print 'Base create'

class childA(Base):
    def __init__(self):
        print 'enter A '
        Base.__init__(self)
        print 'leave A'


class childB(childA, Base):
    def __init__(self):
        childA.__init__(self)
        Base.__init__(self)

b = childB()
```
Base的__init__()方法被执行了两次
```
enter A 
Base create
leave A
Base create
```
使用super()是可避免重复调用
```python
class Base(object):
    def __init__(self):
        print 'Base create'

class childA(Base):
    def __init__(self):
        print 'enter A '
        super(childA, self).__init__()
        print 'leave A'


class childB(childA, Base):
    def __init__(self):
        super(childB, self).__init__()

b = childB()
print b.__class__.mro()
```
```
enter A 
Base create
leave A
[<class '__main__.childB'>, <class '__main__.childA'>, <class '__main__.Base'>, <type 'object'>]
```
