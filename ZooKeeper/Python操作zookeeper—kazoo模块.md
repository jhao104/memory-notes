## 1、安装kazoo

　　kazoo可以直接使用`pip`或者`easy_install`安装:
```
pip install kazoo
```

## 2、基础使用

###2.1 连接

　　使用`KazooClient`对象建立连接：
```
from kazoo.client import KazooClient

zk = KazooClient(hosts='10.10.20.127:4181',
                 timeout=10.0,
                 client_id=None,
                 handler=None,
                 default_acl=None,
                 auth_data=None,
                 read_only=None,
                 randomize_hosts=True,
                 connection_retry=None,
                 command_retry=None,
                 logger=None)
zk.start()
```
　　一旦连接上，客户端会尽力保持连接，不管间歇性的连接丢失。如果要主动丢弃连接，可以使用```zk.stop()```，该方法会断开连接和关闭该连接的session,同时该连接创建的所有临时节点都会立即移除，并触发这些临时节点的DataWatch和这些临时节点的父节点的ChildrenWatch。

* 参数说明：

    * `hosts`: 指定ZooKeeper的ip和端口，可以是以逗号分隔的多个ZooKeeper服务器IP和端口，客户端会随机选择一个来连接;
    * `timeout`: 会话超时时间，在连接断开后就开始计算，如果在此会话时间内重新连接上的话，该连接创建的临时节点就不会移除;
    * `client_id`: 传入一个可切片类型列表或者元组，[会话id, 密码]，用于重新连接先前的会话；
    * `handler`: 传入一个~kazoo.interfaces.IHandler的类实例，用于回调操作；
    * `default_acl`: 创建节点时设置访问控制的模式,类似UNIX的文件访问权限;
    * `auth_data`: 验证证书;
    * `read_only`: 创建一个只读连接;
    * `randomize_hosts`: 随机从hosts中选择一个zk服务器连接;
    * `connection_retry`: 传入kazoo.retry.KazooRetry中的一个类实例，用于重试zk连接；
    * `logger`: 自定义的logger对象，用来替代原有的日志；

### 2.2 日志设置

　　如果代码你没有设置logging，运行时将会提醒你没有log handler:
```
No handlers could be found for logger "kazoo.client"
```
　　除非你在代码中加入日志对象：
```
import logging
logging.basicConfig()
```

### 2.3 zk类属性及方法

* zk.client_state

　　返回客户端连接状态，状态一般有:`AUTH_FAILED`、`CONNECTED`、`CONNECTED_RO`、`CONNECTING`、`CLOSED`、`EXPIRED_SESSION`;

* zk.connected

　　客户端是否已连接到zk服务器，已连接上返回True;

* zk.add_listener(listener)

　　添加一个回调函数，当zk连接状态发生改变时会被调用;

* zk.remove_listener(listener)

　　移出add_listener添加的function;

* zk.start(timeout)

　　初始化到zookeeper服务器的连接，超过timeout时间没连接到zk服务器则会抛出timeout_exception异常，默认时间是15秒;

* zk.stop()

　　关闭连接;

* zk.restart()

　　重新连接zk，内部直接就是先后调用stop()和start();

* zk.close()

　　释放客户端占用的资源，这个方法应该在stop()之前使用;

* zk.command(self, cmd=b'ruok')

　　执行zk服务器的四字命令,传入二进制字符串;常见的命令如下:

| 四字命令  | 功能描述
|---|---|
| conf  |输出相关服务配置的详细信息。|
|cons|列出所有连接到服务器的客户端的完全的连接/会话的详细信息。包括“接受/发送”的包数量、会话 id 、操作延迟、最后的操作执行等等信息。|
|dump|列出未经处理的会话和临时节点。|
|envi|输出关于服务环境的详细信息（区别于 conf 命令）。|
|reqs|列出未经处理的请求|
|ruok|测试服务是否处于正确状态。如果确实如此，那么服务返回“ imok ”，否则不做任何相应。|
|stat|输出关于性能和连接的客户端的列表。|
|wchs|列出服务器 watch 的详细信息。|
|wchc|通过 session 列出服务器 watch 的详细信息，它的输出是一个与 watch 相关的会话的列表。|
|wchp|通过路径列出服务器 watch 的详细信息。它输出一个与 session 相关的路径。|

* zk.sync(path)

　　阻塞并等待指定节点同步到所有zk服务器，返回同步的节点;

* zk.create(path, value=b"")

　　创建一个新的节点，节点数据为value;

* zk.ensure_path(path)

　　如何这个节点的父节点不存在，自动创建父节点路径;

* zk.exists(path,watch=None)

　　检查节点是否存在，存在返回节点的ZnodeStat信息，否则返回None。可传入回调方法watch,当节点create/delete或是set的时候该方法会被调用

* zk.get(path)

　　获取节点值。

* zk.get_children(path)

　　获取所有子节点，返回列表形式。

* zk.set(path, value)

　　设置节点的值。

* zk.delete(path recursive=False) 

　　删除节点，recursive为True表示递归删除节点及其子节点，如果有子节点且recursive为False，则会产生NotEmptyError异常，表示该节点有子节点不能删除


### 2.4 监听连接事件

　　可用来知道ZooKeeper连接删除、恢复或者过期的消息。为了简化这个过程，Kazoo使用一个状态系统，并允许你注册监听函数，以便在状态改变时被调用。
```
from kazoo.client import KazooState

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
    else:
        # Handle being connected/reconnected to Zookeeper

zk.add_listener(my_listener)
```
　　当使用`kazoo.recipe.lock.Lock`或创建临时节点时，最好添加一个状态监听器，以便在连接中断或Zookeeper会话丢失时做出应对动作。

### 2.5 Kazoo状态

　　`KazooState`对象表示客户端链接的几个状态。客户端的当前状态总是可以通过查看state属性来确定。可能的状态有：

* LOST

* CONNECTED

* SUSPENDED

　　首次创建KazooClient实例时，它处于LOST状态。建立连接后，它将转换到CONNECTED状态。如果出现连接问题或者需要连接到其他的Zookeeper集群节点，状态将转换为SUSPENDED，此时无法执行任何命令。如果Zookeeper节点不再是Quorum的一部分，连接也将丢失，状态置为SUSPENDED。

　　再重新建立连接时，如果会话已经过期，则客户端可以转换到LOST，或者如果会话仍然有效，则客户端可以转换为CONNECTED。

> 注：在实际应用中最好使用前文提出的监听函数监视这些状态，以便客户端根据连接的状态正确运行。

　　当连接状态为SUSPENDED时，此时客户端应当暂停执行需要与其他系统协议的操作（例如分布式锁），当连接重新建立后，如果状态转换为CONNECTED才可以继续。当连接状态为LOST时，Zookeeper将删除已创建的任何临时节点。这会影响创建临时节点的所有recipes。

#### 状态转换

* LOST -> CONNECTED

　　建立新连接，或丢失的连接恢复。

* CONNECTED -> SUSPENDED

　　Connection丢失了服务端的连接。

* CONNECTED -> LOST

　　仅在连接建立后提供无效的身份验证凭证时才会发生。

* SUSPENDED -> LOST

　　Connection服务端已恢复，但是会话已过期而丢失。

* SUSPENDED -> CONNECTED

    丢失的连接已恢复。
    
### 2.5 只读模式

　　ZooKeeper3.4及以上版本支持[只读模式](https://wiki.apache.org/hadoop/ZooKeeper/GSoCReadOnlyMode)。只有ZooKeeper集群服务启用此模式，客户端才能使用它。只要将KazooClient的read_only设置为True便可以使客户端连接到只读的Zookeeper节点。

```
from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181', read_only=True)
zk.start()
```
