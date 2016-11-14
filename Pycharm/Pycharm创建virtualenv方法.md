
>Python的版本众多,在加上适用不同版本的Python Package。这导致在同时进行几个项目时，对库的依赖存在很大的问题。这个时候就牵涉到对Python以及依赖库的版本管理，方便进行开发，virtualenv就是用来解决这个问题的。下面介绍使用PyCharm创建Virtual Environment的方法。

　　PyCharm可以使用[virtualenv](https://virtualenv.pypa.io/en/latest/index.html)中的功能来创建虚拟环境。PyCharm紧密集成了virtualenv，所以只需要在setting中配置即可创建虚拟环境。而且PyCharm捆绑了virtualenv，我们不需要单独安装。一般创建过程如下：

* 1、打开Project Interpreters页面：文件(file)——>设置(setting)——>项目(Project)——>Project Interpreters；
　　![](http://ofcf9jxzt.bkt.clouddn.com/blog/pycharm/1.png)

* 2、选择项目，点击右边的配置按钮![配置](https://www.jetbrains.com/help/img/idea/cogwheel_framed.png)，选择**Create VirtualEnv**。这时会弹出**Create Virtual Environment**的对话框；

* 3、配置新环境：

    * **Name**中填写新虚拟环境的名字，或者使用默认名字，方便以后安装第三方包和其他项目使用；
    
    * 在**Location**中填写新环境的文件目录;
    
    * 在**Base interpreter**下拉框中选择Python解释器；
   
    * 勾选**Inherit global site-packages**可以使用base interpreter中的第三方库，不选将和外界完全隔离；
    
    * 勾选**Make available to all projects**可将此虚拟环境提供给其他项目使用。

* 4、点击OK，一切配置完毕。这样是不是比单独配置virtualenv简单的多。
　　![](http://ofcf9jxzt.bkt.clouddn.com/blog/pycharm/2.png)
    
