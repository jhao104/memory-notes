## 安装kazoo

　　kazoo可以直接使用`pip`或者`easy_install`安装:
```
pip install kazoo
```

## 基础使用

### 连接
　　使用`KazooClient`对象建立连接：
```
from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181')
# 多个地址用逗号间隔
zk.start()
```
　　一旦连接上，客户端会尽力保持连接，不管间歇性的连接丢失。如果要主动丢弃连接，可以使用```zk.start()```，该方法会断开连接和关闭该连接的session。


[cankao](http://sapser.github.io/python/zookeeper/2014/07/24/zookeeper-kazoo)