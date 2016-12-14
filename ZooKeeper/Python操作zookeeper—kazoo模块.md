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




未完成
<!--[cankao](http://sapser.github.io/python/zookeeper/2014/07/24/zookeeper-kazoo)-->