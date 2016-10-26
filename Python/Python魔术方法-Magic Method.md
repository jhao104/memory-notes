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

