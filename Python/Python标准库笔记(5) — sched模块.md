## 事件调度
　　`sched`模块内容很简单，只定义了一个类。它用来最为一个通用的事件调度模块。

　　`class sched.scheduler(timefunc, delayfunc)`这个类定义了调度事件的通用接口，它需要外部传入两个参数，`timefunc`是一个没有参数的返回时间类型数字的函数(常用使用的如time模块里面的time)，`delayfunc`应该是一个需要一个参数来调用、与timefunc的输出兼容、并且作用为延迟多个时间单位的函数(常用的如time模块的sleep)。

　　下面是一个列子:
```python
import sched, time

s = sched.scheduler(time.time, time.sleep)  # 生成调度器

def print_time():
    print "From print_time", time.time()

def print_some_times():
    print time.time()
    s.enter(5, 1, print_time, ())  
    # 加入调度事件
    # 四个参数分别是:
    #    间隔事件(具体值决定与delayfunc, 这里为秒);
    #    优先级(两个事件在同一时间到达的情况);
    #    触发的函数;
    #    函数参数；
    s.enter(10, 1, print_time, ())
    
    # 运行
    s.run()
    print time.time()

if __name__ == '__main__':
    print_some_times()
```
　　看到的输出结果，隔5秒中执行第一个事件,隔10秒后执行第二个事件：
```python
1499259731.99
From print_time 1499259736.99
From print_time 1499259741.99
1499259741.99
```

　　在多线程场景中，会有线程安全问题，run()函数会阻塞主线程。官方建议使用`threading.Timer`类代替:

```python
import time
from threading import Timer

def print_time():
    print "From print_time", time.time()

def print_some_times():
    print time.time()
    Timer(5, print_time, ()).start()
    Timer(10, print_time, ()).start()
    time.sleep(11)  # 阻塞主线程,等待调度程序执行完毕，再执行后面内容
    print time.time()

if __name__ == '__main__':
    print_some_times()
```

## Scheduler对象方法

　　scheduler对象拥有下面这些方法或属性:

* scheduler.enterabs(time, priority, action, argument)

　　加入一个事件,`time`参数应该是一个与传递给构造函数的`timefunc`函数的返回值相兼容的数值类型。在同一时间到达的事件将按照`priority`顺序执行。

　　执行事件其实就是执行`action(argument)`。argument必须是一个包含`action`参数的序列。

　　返回值是一个事件，它可以用于稍后取消事件(请参见`cancel()`)。

* scheduler.enter(delay, priority, action, argument)

　　安排一个事件来延迟`delay`个时间单位。除了时间外，其他参数、含义和返回值与`enterabs()`的值相同。其实内部`enterabs`就是用来被`enter`调用。

* scheduler.cancel(event)

　　从队列中删除事件。如果事件不是当前队列中的事件，则该方法将跑出一个`ValueError`。

* scheduler.empty()

　　判断队列是否为空。

* scheduler.run()

　　运行所有预定的事件。这个函数将等待(使用传递给构造函数的`delayfunc()`函数)，然后执行事件，直到不再有预定的事件。

　　任何`action`或`delayfunc`都可以引发异常。在这两种情况下，调度器将保持一个一致的状态并传播异常。如果一个异常是由`action`引起的，就不会再继续执行`run()`。

* scheduler.queue

　　只读属性，返回一个即将到达的事件列表(按到达事件排序)，每个事件都是有`time`、`priority`、`action`、`argument`组成的`namedtuple`。

