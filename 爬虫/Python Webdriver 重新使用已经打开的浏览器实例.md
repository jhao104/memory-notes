因为Webdriver每次实例化都会新开一个全新的浏览器会话，在有些情况下需要复用之前打开未关闭的会话。比如爬虫，希望结束脚本时，让浏览器处于空闲状态。当脚本重新运行时，它将继续使用这个会话工作。还就是在做自动化测试时，前面做了一大推操作，但是由于程序出错，重启时不用再继续前面复杂的操作。

个人觉得这种功能非常有用，但是官方居然没有提供这种功能的API，苦苦搜搜，在网上找了两个java版的http://blog.csdn.net/wwwqjpcom/article/details/51232302 和 http://woxiangbo.iteye.com/blog/2372683
看了下源码其实java和python的驱动原理过程都非常相似。

打开一个Chrome会话:
```python
from selenium import webdriver
driver = webdriver.Chrome()
```
运行上面的脚本，它将启动浏览器并退出。因为没有调用`quit()`方法，所以浏览器会话仍会存在。但是代码里创建的`driver`对象已经不在了，理论上不能用脚本控制这个浏览器。它将变成一个僵尸浏览器，只能手动杀死它。

通过webdriver启动一个浏览器会话大概会有这样三个阶段:

* 1、启动的浏览器驱动代理(hromedriver，Firefox的驱动程序，等等)；
* 2、创建一个命令执行器。用来向代理发送操作命令；
* 3、使用代理建立一个新的浏览器会话，该代理将与浏览器进行通信。用`sessionId`来标识会话。

因此只要拿到阶段2中的执行器和阶段3中的`sessionID`就能恢复上次的会话。这两个有api可以直接获取:
```python
from selenium import webdriver

driver = webdriver.Chrome()
executor_url = driver.command_executor._url
session_id = driver.session_id
print(session_id)
print(executor_url)
driver.get("http://www.spiderpy.cn/")
```

得到类似这样的输出（第一个是会话的sessionId,第二个就是命令执行器连接）：
```shell
397d725f042a076f7d4a82f7d3fead13
http://127.0.0.1:52869
```

一切就绪，下面就开始实现复用之前会话的功能，在[Stack Overflow](https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session)上面讲的实现是这样的:
```python
from selenium import webdriver

driver = webdriver.Chrome()
executor_url = driver.command_executor._url
session_id = driver.session_id
driver.get("http://www.spiderpy.cn/")

print(session_id)
print(executor_url)

driver2 = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
driver2.session_id = session_id
print(driver2.current_url)
```
可能是因为版本原因吧，反正在我环境中运行时，效果是实现了，能够重新连接到上一个会话，但是却打开了一个新的空白会话。看了下`Remote`类的源码，发现是因为每次实例化都会调用`start_session`这个方法新建一个会话。所以解决方法就是继承并重写这个类。自定义一个`ReuseChrome`这个类重写`start_session`方法使它不再新建session，使用传入的session_id：
```python
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException


class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
```

然后在第二次连接是使用重写的`ReuseChrome`类：
```python
from selenium import webdriver

#  第一次使用Chrome() 新建浏览器会话
driver = webdriver.Chrome()

# 记录 executor_url 和 session_id 以便复用session
executor_url = driver.command_executor._url
session_id = driver.session_id
# 访问百度
driver.get("http://www.spiderpy.cn/")

print(session_id)
print(executor_url)

# 假如driver对象不存在，但浏览器未关闭
del driver

# 使用ReuseChrome()复用上次的session
driver2 = ReuseChrome(command_executor=executor_url, session_id=session_id)

# 打印current_url为百度的地址，说明复用成功
print(driver2.current_url)
driver2.get("https://www.baidu.com")
```

这样就能顺利连接到上次没关闭的浏览器会话。