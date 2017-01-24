在本教程中，我们将引导您完成一个投票应用程序的创建，它包含下面两部分：

* 一个可以进行投票和查看结果的公开站点；

* 一个可以进行增删改查的后台admin管理界面；

我们假设你已经安装了Django。您可以通过运行以下命令来查看Django版本以及验证是否安装：

```
python -m django --version
```

如果安装了Django，您应该将看到安装的版本。如果没有安装，你会得到一个错误，提示`No module named django`。

本教程是为Django 1.10和Python 3.4或更高版本编写的。如果Django版本不匹配，您可以去官网参考您的对应Django版本的教程，或者将Django更新到最新版本。

如果你仍然在使用Python 2.7，你需要稍微调整代码，注意代码中的注释。

## 创建project

如果这是你第一次使用Django，你将需要处理一些初始设置。也就是说，这会自动生成一些建立Django项目的代码，但是你需要设置一些配置，包括数据库配置，Django特定的选项和应用程序特定的设置等等。

从命令行，`cd`进入您将存放项目代码的目录，然后运行以下命令:

```
django-admin startproject mysite  # mysite为项目名
```

如果运行出错，请参见[Problems running django-admin](https://docs.djangoproject.com/en/1.10/faq/troubleshooting/#troubleshooting-django-admin)。这将在目录下生成一个mysite目录，也就是你的这个Django项目的根目录。它包含了一系列自动生成的目录和文件，具备各自专有的用途。

> 注意: 在给项目命名的时候必须避开Django和Python的保留关键字。比如“django”（它会与Django本身冲突）或“test”（它与一个内置的Python包冲突）。

> 这些代码应该放在哪儿？ 如果你曾经学过普通的旧式的PHP（没有使用过现代的框架），你可能习惯于将代码放在Web服务器的文档根目录下（例如/var/www）。使用Django时，建议你不要这么做。 将Python代码放在你的Web服务器的根目录不是个好主意，因为这可能会有让其他人看到你的代码的风险。

一个新建立的项目结构大概如下：
```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```

这些文件分别是:

* 外层的mysite/根目录仅仅是项目的一个容器。它的命名对Django无关紧要；你可以把它重新命名为任何你喜欢的名字;

* manage.py：一个命令行工具，可以使你用多种方式对Django项目进行交互。 你可以在[django-admin和manage.py](https://docs.djangoproject.com/en/1.10/ref/django-admin/)中读到关于manage.py的所有细节;

* 内层的mysite/目录是你的项目的真正的Python包。它的名字是你引用内部文件的包名（例如 mysite.urls）;

* `mysite/__init__.py`：一个空文件，它告诉Python这个目录应该被看做一个Python包;

* mysite/settings.py：该Django项目的配置文件。具体内容可以参见[Django settings](https://docs.djangoproject.com/en/1.10/topics/settings/);

* mysite/urls.py: 路由文件,相当于你的Django站点的“目录”。 你可以在[URL转发器](https://docs.djangoproject.com/en/1.10/topics/http/urls/)中阅读到关于URL的更多内容;

* mysite/wsgi.py：用于你的项目的与WSGI兼容的Web服务器入口。用作服务部署，更多细节请参见[如何利用WSGI进行部署](https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/)。


## 开发服务器

让我们验证一下你的Django项目是否工作。 进入外层的mysite目录，然后运行以下命令:
```
python manage.py runserver
```

你将在看到如下输出:
```
Performing system checks...

System check identified no issues (0 silenced).

You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
January 09, 2017 - 16:22:02
Django version 1.10.2, using settings 'Django_learn.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

> 注意：现在忽略有关未应用数据库迁移的警告;下面教程将很快处理数据库

这表明你已经启动了Django开发服务器，一个用纯Python写的轻量级Web服务器。 我们在Django中内置了它，这样你就可以在不配置用于生产环境的服务器（例如Apache）的情况下快速开发出产品，直到你准备好上线。

请注意：不要在任何生产环境使用这个服务器。它仅仅是用于在开发中使用。（我们的重点是编写Web框架，非Web服务器。）

既然服务器已经运行，请用你的浏览器访问 http://127.0.0.1:8000。 在淡蓝色背景下，你将看到一个“Welcome to Django”的页面。 It worked!


### 修改端口号

默认情况下，runserver命令在内部IP的8000端口启动开发服务器。

如果你需改变服务器的端口，把要使用的端口作为一个命令行参数传递给它。 例如，这个命令在8080端口启动服务器：

```
python manage.py runserver 8080
```

如果你需改变服务器的IP地址，把IP地址和端口号放到一起。 因此若要监听所有的外网IP，请使用（如果你想在另外一台电脑上展示你的工作，会非常有用）：

```
python manage.py runserver 0.0.0.0:8000
```

### runserver的自动重载

在Debug模式下，开发服务器会根据需要自动重新载入Python代码。 你不必为了使更改的代码生效而重启服务器。 然而，一些行为比如添加文件，不会触发服务器的重启，所以在这种情况下你需要手动重启服务器。

## 创建投票app

你编写的每个Django应用都是遵循特定约定且包含一个Python包。 Django自带这个功能，它可以自动生成应用的基本目录结构（就像创建项目那样）

project和app区别：

* 一个app实现某个功能，比如博客、公共档案数据库或者简单的投票系统；

* 一个project是配置文件和多个app的集合，他们组合成整个站点；

* 一个project可以包含多个app；

* 一个app可以属于多个project。

app的存放位置可以是任何地点，但是通常我们将它们都放在与manage.py同级目录下，这样方便导入文件。

进入mysite目录，确保与manage.py文件处于同一级，并且键入以下命令来创建你的app:

```
python manage.py startapp polls  # polls为app的name
```

这将创建一个目录polls，它的结构如下：

```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

## 编写视图

让我们写第一个视图。打开文件polls/views.py，并输入以下Python代码：
```python
# polls/views.py
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```
这是Django中最简单的视图。要调用视图，我们需要将它映射到一个URL,为此，我们需要一个URLconf。

要在polls目录中创建一个URLconf，在polls文件夹中创建一个名为urls.py的文件。您的应用目录现在应该像这样:
```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
```

编辑polls/urls.py文件：
```python
# polls/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
```

你可以看到项目根目录下的mysite目录也有个urls.py文件，下一步是让这个项目的主urls.py文件指向我们建立的polls这个app独有的urls.py文件，打开mysite/urls.py文件，你需要先导入include模块，代码如下：
```python
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
```

include语法相当于二级路由策略，它将接收到的url地址去除了它前面的正则表达式，将剩下的字符串传递给下一级路由进行判断。

include的背后是一种即插即用的思想。项目根路由不关心具体app的路由策略，只管往指定的二级路由转发，实现了解耦的特性。app所属的二级路由可以根据自己的需要随意编写，不会和其它的app路由发生冲突。app目录可以放置在任何位置，而不用修改路由。这是软件设计里很常见的一种模式。

您现在已将索引视图连接到URLconf。让我们验证它的工作，运行以下命令：

```
python manage.py runserver
```

在浏览器中访问http//localhost8000/polls/，你应该看到文本“Hello, world. You're at the polls index.“，就如你在view.py中定义的那样。

url()函数可以传递4个参数，其中2个是必须的：regex和view，以及2个可选的参数：kwargs和name。下面是具体的解释：

### url() 参数：regex

regex是正则表达式的通用缩写，它是一种匹配字符串或url地址的语法。Django拿着用户请求的url地址，在urls.py文件中对urlpatterns列表中的每一项条目从头开始进行逐一对比，一旦遇到匹配项，立即执行该条目映射的视图函数或二级路由，其后的条目将不再继续匹配。因此，url路由的编写顺序至关重要！

需要注意的是，regex不会去匹配GET或POST参数或域名，例如对于https://www.example.com/myapp， regex只尝试匹配myapp/。对于https://www.example.com/myapp/?page=3， regex也只尝试匹配myapp/

### url() 参数：view

当正则表达式匹配到某个条目时，自动将封装的HttpRequest对象作为第一个参数，正则表达式“捕获”到的值作为第二个参数，传递给该条目指定的视图。如果是简单捕获，那么捕获值将作为一个位置参数进行传递，如果是命名捕获，那么将作为关键字参数进行传递。

### url() 参数：kwargs

任意数量的关键字参数可以作为一个字典传递给目标视图。

### url() argument: name

对你的URL进行命名，可以让你能够在Django的任意处，尤其是模板内显式地引用它。相当于给URL取了个全局变量名，你只需要修改这个全局变量的值，在整个Django中引用它的地方也将同样获得改变。这是极为古老、朴素和有用的设计思想，而且这种思想无处不在。


