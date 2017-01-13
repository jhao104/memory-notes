本教程继续Part1。我们将设置数据库，创建您的第一个模型，并快速介绍Django的自动生成的管理网站。

## 数据库设置

现在，编辑`mysite/settings.py`。它是一个用模块级别变量表示Django配置的普通Python模块。

Django的默认数据库是SQLite。如果你是数据库初学者，或者你只是想要试用一下Django，SQLite是最简单的选择。 SQLite包含在Python中，所以你不需要另外安装其他任何东西。当然在你开始第一个真正的项目时，你可能想使用一个更健壮的数据库比如PostgreSQL来避免在未来遇到令人头疼的数据库切换问题。

如果你希望使用另外一种数据库，请配置合适的database binding，并在`mysite/settings.py`的DATABASES 'default'条目中修改以下的配置以匹配你的数据库连接的设置：

* ENGINE-支持'django.db.backends.sqlite3', 'django.db.backends.postgresql_psycopg2', 'django.db.backends.mysql'或'django.db.backends.oracle'；

* NAME-数据库的名称。如果你使用SQLite，数据库将是你计算机上的一个文件； 如果是这样的话，NAME应该是这个文件的绝对路径，包括文件名。默认值是os.path.join(BASE_DIR, 'db.sqlite3')，它将文件保存在你项目的目录中；

* 如果不使用SQLite作为数据库，则必须添加其他设置，例如[USER](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-USER)，[PASSWORD](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-PASSWORD)和[HOST](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-HOST)。有关更多详细信息，请参阅[DATABASES](https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-DATABASES)的参考文档。

> 注：如果你使用PostgreSQL或者MySQL，确保到此你已经建立好一个数据库。如果你使用SQLite，你不需要事先创建任何东西。

当你编辑`mysite/settings.py`时，请设置TIME_ZONE为你自己的时区。

`INSTALLED_APPS `中是Django实例中所有Django应用的名称。应用可以在多个项目中使用，而且你可以将这些应用打包和分发给其他人在他们的项目中使用。

`INSTALLED_APPS `默认包含了一下应用:

* django.contrib.admin —— 管理站点；

* django.contrib.auth —— 用户认证系统；

* django.contrib.contenttypes —— 用于内容类型的框架；

* django.contrib.sessions —— 会话框架；

* django.contrib.messages —— 消息框架；

* django.contrib.staticfiles —— 管理静态文件的框架。

这些应用，默认包含在Django中，以方便通用场合下使用。

其中一些应用程序使用至少一个数据库表，所以我们需要在数据库中创建表，然后才能使用它们。为此，请运行以下命令：

```
python manage.py migrate
```

migrate查看INSTALLED_APPS设置并根据mysite/settings.py文件中的数据库设置创建任何必要的数据库表，数据库的迁移还会跟踪应用的变化。你会看到对每次迁移有一条信息。如果你有兴趣，可以运行你的数据库的命令行客户端并输入dt (PostgreSQL), SHOW TABLES; (MySQL)或.schema (SQLite)来显示Django创建的表。

>对于极简主义者来说:INSTALLED_APPS包含的默认应用用于常见的场景，但并不是每个人都需要它们。 如果你不需要它们中的任何一个或所有应用，可以在运行migrate之前从INSTALLED_APPS中自由地注释或删除相应的行。migrate 命令将只为INSTALLED_APPS中的应用运行数据库的迁移。

## 创建模型

现在定义该应用的模型——本质上，就是定义该模型所对应的数据库设计及其附带的元数据。

在这个投票应用中，我们将创建两个模型： Question和Choice。Question对象具有一个question_text（问题）属性和一个publish_date（发布时间）属性。 Choice有两个字段：选择的内容和选择的得票统计。 每个Choice与一个Question关联。

这些概念通过简单的Python类来表示。 编辑polls/models.py文件，并让它看起来像这样：
```
# polls/models.py
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
代码很简单。每个模型由一个子类django.db.models.Model的类表示。每个模型都有一些类变量，每个变量表示模型中的数据库字段。

每个字段由Field类的实例表示，例如，字符串类型字段的CharField和数据时间类型的DateTimeField。这告诉Django每个字段持有什么类型的数据。

每个字段实例的名称（例如question_text或pub_date）就是字段的名称，以机器友好的形式。您将在Python代码中使用此值，您的数据库将使用它作为列名称。

您可以使用字段的可选第一个位置参数来指定一个更通俗的名称。这在Django的一些内省部分中使用，它也可以作为文档。如果不提供此字段，Django将使用机器可读的名称。在这个例子中，我们只为Question.pub_date定义了一个通俗的名称。对于此模型中的所有其他字段，该字段的机器可读名称将足以作为其通俗名称。

有些Field类具有必需的参数。例如，CharField要求你给它一个max_length。这不仅在数据库模式中使用，而且在验证中使用。

Field还可以有各种可选参数;在上例中，我们将votes的默认值设置为0。

最后，使用ForeignKey定义关系。这告诉Django每个选择是与单个问题相关。 Django支持所有常见的数据库关系：多对一，多对多和一对一。

## 激活模型

上面那段简短的模型代码给了Django很多信息。 有了这些代码，Django就能够：

* 为该应用创建数据库表（CREATE TABLE 语句）；

* 为Question对象和Choice对象创建一个访问数据库的python API。

但是首先得在INSTALLED_APPS中添加此应用。

> 理念: Django应用程序是“即插式”的：您可以在多个项目中使用应用程序，并且您可以分发应用程序，因为他们不必绑定到给定的Django安装。

要在我们的项目中包含应用程序，我们需要在INSTALLED_APPS设置中添加对其配置类的引用。 PollConfig类位于polls/aps.py文件中，因此其虚线路径为“polls.apps.PollsConfig”。编辑mysite/settings.py文件，并将该虚线路径添加到INSTALLED_APPS设置。它看起来像这样:

```
#  mysite/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig'
]
```
现在Django包含了polls应用，下面运行:

```
python manage.py makemigrations polls
```

将会看到如下输出:
```
Migrations for 'polls':
  polls\migrations\0001_initial.py:
    - Create model Choice
    - Create model Question
    - Add field question to choice

```
通过运行makemigrations告诉Django，已经对模型做了一些更改（在这个例子中，你创建了一个新的模型）并且会将这些更改存储为迁移文件。

迁移是Django储存模型的变化（以及您的数据库模式），它们只是磁盘上的文件。如果愿意，你可以阅读这些为新模型建立的迁移文件；这个迁移文件就是polls/migrations/0001_initial.py。不用担心，Django不要求你在每次Django生成迁移文件之后都要阅读这些文件，但是它们被设计成可人为编辑的形式，以便你可以手工稍微修改一下Django的某些具体行为。

有一个命令可以运行这些迁移文件并自动管理你的数据库模式——migrate，我们一会儿会用到它。但是首先，让我们看一下迁移行为将会执行哪些SQL语句。sqlmigrate命令接收迁移文件的名字并返回它们的SQL语句：

```
python manage.py sqlmigrate polls 0001
```

你应该会看到类似如下的内容（为了便于阅读我们对它重新编排了格式）：
```
BEGIN;
CREATE TABLE "polls_choice" (
    "id" serial NOT NULL PRIMARY KEY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL
);
CREATE TABLE "polls_question" (
    "id" serial NOT NULL PRIMARY KEY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
ALTER TABLE "polls_choice" ADD COLUMN "question_id" integer NOT NULL;
ALTER TABLE "polls_choice" ALTER COLUMN "question_id" DROP DEFAULT;
CREATE INDEX "polls_choice_7aa0f6ee" ON "polls_choice" ("question_id");
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_246c99a640fbbd72_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;

COMMIT;
```

注意以下几点:

* 输出的具体内容会依据你使用的数据库而不同。 以上例子使用的数据库是PostgreSQL;

* 表名是自动生成的，由app的名字（polls）和模型名字的小写字母组合而成 —— question和choice(你可以重写这个行为);

* 主键（IDs）是自动添加的。 （你也可以重写这个行为);

* 按照惯例，Django会在外键的字段名后面添加 "_id"。（你依然可以重写这个行为）;

* 外键关系由FOREIGN KEY约束显式声明。不用在意DEFERRABLE部分；它只是告诉PostgreSQL直到事务的最后再执行外键关联;

* 这些SQL语句是针对你所使用的数据库定制的，所以会为你自动处理某些数据库所特有的字段例如auto_increment (MySQL)、 serial (PostgreSQL)或integer primary key autoincrement (SQLite) 。在处理字段名的引号时也是如此 —— 例如，使用双引号还是单引号;

* sqlmigrate命令并不会在你的数据库上真正运行迁移文件 —— 它只是把Django 认为需要的SQL打印在屏幕上以让你能够看到。 这对于检查Django将要进行的数据库操作或者你的数据库管理员需要这些SQL脚本是非常有用的。

如果你有兴趣，你也可以运行`python manage.py check`;这将检查您的项目中的任何问题，而不进行迁移或触摸数据库。

现在，再次运行migrate以在你的数据库中创建模型所对应的表:

```
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Rendering model states... DONE
  Applying polls.0001_initial... OK
```

migrate命令会找出所有还没有被应用的迁移文件（Django使用数据库中一个叫做django_migrations的特殊表来追踪哪些迁移文件已经被应用过），并且在你的数据库上运行它们。就是使你的数据库模式和你改动后的模型进行同步。

迁移功能非常强大，可以让你在开发过程中不断修改你的模型而不用删除数据库或者表然后再重新生成一个新的 —— 它专注于升级你的数据库且不丢失数据。 我们将在本教程的后续章节对迁移进行深入地讲解，但是现在，请记住实现模型变更的三个步骤：

* 修改你的模型（在models.py文件中）；

* 运行`python manage.py makemigrations`，为这些修改创建迁移文件；

* 运行`python manage.py migrate`，将这些改变更新到数据库中;

阅读[django-admin](http://python.usyiyi.cn/documents/django_182/ref/django-admin.html) 的文档来了解manage.py 工具能做的所有事情。

## 使用API

现在，进入Python的交互式shell，玩转这些Django提供给你的API。 使用如下命令来调用Python shell：

```
python manage.py shell
```

我们使用上述命令而不是简单地键入“python”进入python环境，是因为manage.py 设置了`DJANGO_SETTINGS_MODULE`环境变量，该环境变量告诉Django导入mysite/settings.py文件的路径。

> 绕过manage.py: 果你不想使用manage.py，只要设置DJANGO_SETTINGS_MODULE 环境变量为 mysite.settings，启动一个普通的Python shell，然后建立Django：
```
>>> import django
>>> django.setup()
```
如果以上命令引发了一个AttributeError，可能是你使用了一个和本教程不匹配的Django版本。 你可能需要换一个老一点的教程或者换一个新一点的Django版本。
您必须从manage.py所在的同一目录运行python，或确保该目录在Python搜索路径中，这个import mysite才会成功。

当你进入shell后，尝试一下下面的API吧：
```
>>> from polls.models import Question, Choice   # 导入我们写的模型类

# question为空
>>> Question.objects.all()
<QuerySet []>

# 新建一个Question
# 在默认设置文件中启用对时区的支持, Django推荐使用timezone.now()代替python内置的datetime.datetime.now()
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# 调用save()方法，将内容保存到数据库中
>>> q.save()

# 默认情况，你会自动获得一个自增的名为id的主键
>>> q.id
1

# 通过python的属性调用方式，访问模型字段的值
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

# 通过修改属性来修改字段的值，然后调用save方法进行保存。
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() 用于查询数据库内的所有questions
>>> Question.objects.all()
<QuerySet [<Question: Question object>]>
```

`<Question: Question object>`对于这个对象是一个不可读的内容展示，你无法从中获得任何直观的信息。 让我们来修复这个问题，让Django在打印对象时显示一些我们指定的信息。编辑Question模型（在polls/models.py文件中）并添加一个__str__()方法给Question和Choice：
```
# polls/models.py
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # 当你想支持python2版本的时候才需要这个装饰器
class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

@python_2_unicode_compatible  # 当你想支持python2版本的时候才需要这个装饰器
class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text
```

在模型中添加`__str __()`方法非常重要，不仅仅是为了方便您处理交互式提示时，而且在Django自动生成的管理界面中也能使用。

注意这些都是普通Python方法。让我们演示一下如何添加一个自定义的方法：

```
# polls/models.py
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```
注意import datetime 和from django.utils import timezone分别引用Python 的标准datetime 模块和Django django.utils.timezone中时区相关的工具。如果你不了解Python中时区的处理方法，你可以在[时区支持](https://docs.djangoproject.com/en/1.10/topics/i18n/timezones/)的文档中了解更多的知识

保存修改后，我们重新启动一个新的python shell ` python manage.py shell`，再来看看其他的API：
```
>>> from polls.models import Question, Choice

# 添加__str__() 后的效果.
>>> Question.objects.all()
<QuerySet [<Question: What's up?>]>

# Django提供了大量的关键字参数查询API
>>> Question.objects.filter(id=1)
<QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
<QuerySet [<Question: What's up?>]>

# 获取今年发布的问卷
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>

# 查询一个不存在的ID，会抛出异常
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.

# Django为主键查询提供了一个缩写：pk。下面的语句和Question.objects.get(id=1)效果一样.
>>> Question.objects.get(pk=1)
<Question: What's up?>

# 看看我们自定义的方法用起来怎么样
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True

# 让我们试试主键查询
>>> q = Question.objects.get(pk=1)

# 显示所有与q对象有关系的choice集合，目前是空的，还没有任何关联对象。
>>> q.choice_set.all()
<QuerySet []>

# C创建3个choices.
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

# Choice对象可通过API访问和他们关联的Question对象
>>> c.question
<Question: What's up?>

# 同样的，Question对象也可通过API访问关联的Choice对象
>>> q.choice_set.all()
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
3

# API会自动进行连表操作，通过双下划线分割关系对象。连表操作可以无限多级，一层一层的连接。
# 下面是查询所有的Choices，它所对应的Question的发布日期是今年。（重用了上面的current_year结果）
>>> Choice.objects.filter(question__pub_date__year=current_year)
<QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# 使用delete方法删除对象
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
```

有关模型关系的更多信息，请参阅[Accessing related objects](https://docs.djangoproject.com/en/1.10/ref/models/relations/)。有关如何使用双下划线通过API执行字段查找的更多信息，请参阅[字段查找](https://docs.djangoproject.com/en/1.10/topics/db/queries/#field-lookups-intro)。有关数据库API的完整详细信息，请参阅我们的[数据库API参考](https://docs.djangoproject.com/en/1.10/topics/db/queries/)。

##  Django admin管理站点介绍

为您的员工或客户生成管理网站用来添加，更改和删除内容是繁琐的工作，不需要太多的创造力。因此，Django完全自动创建模型的管理界面。
Django是在一个新闻编辑室的环境中编写的，“内容发布者”和“公共”网站之间有着非常明确的区分。
网站管理员使用系统添加新闻故事，事件，体育等，并且该内容显示在公共网站上。 
Django解决了为网站管理员创建统一界面以编辑内容的问题。管理网站不打算供网站访问者使用。

## 创建管理用户

首先，我们需要创建一个可以登录到管理网站的用户。运行以下命令：
```
python manage.py createsuperuser
```
输入用户名：
```
Username: admin
```
输入邮箱地址：
```
Email address: admin@example.com
```
最后一步是输入您的密码。您将被要求输入您的密码两次，第二次作为第一次确认。
```
Password: **********
Password (again): *********
Superuser created successfully.
```

## 启动开发服务器

Django的管理站点是默认启用的。 让我们启动开发服务器：
```
python manage.py runserver
```
现在，打开Web浏览器并转到您本地域的“/ admin /”，例如，http://127.0.0.1:8000/admin/。 您应该会看到管理员的登录界面：
![login](http://images2015.cnblogs.com/blog/1039209/201701/1039209-20170112201603478-1380872513.png)

由于翻译是默认打开的，登录界面可能会以您自己的语言显示，具体取决于您的浏览器设置，以及Django是否有此语言的翻译。

### 进入admin站点

使用在上一步中创建的超级用户帐户登录。您应该会看到Django管理员索引页面：
![site](http://images2015.cnblogs.com/blog/1039209/201701/1039209-20170112201652338-954873099.png)
您应该会看到几种类型的可编辑内容：组和用户。它们由django.contrib.auth提供，Django提供的认证框架。

### 使应用在管理站点可编辑

现在你还无法看到你的投票应用，必须先在admin中进行注册，告诉admin站点，请将poll的模型加入站点内，接受站点的管理。

打开polls/admin.py文件，加入下面的内容：
```
# polls/admin.py
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

### 浏览admin站点的功能
注册question模型后，刷新admin页面就能看到Question栏目:
![question1](http://images2015.cnblogs.com/blog/1039209/201701/1039209-20170112201712697-1579416884.png)

点击“Questions”，进入questions的修改列表页面。这个页面会显示所有的数据库内的questions对象，你可以在这里对它们进行修改。看到下面的“What’s up?”了么？它就是我们先前创建的一个question，并且通过__str__方法的帮助，显示了较为直观的信息，而不是一个冷冰冰的对象类型名称。

![question2](http://images2015.cnblogs.com/blog/1039209/201701/1039209-20170112201720431-1694701348.png)

点击What’s up?进入编辑界面：
![question3](http://images2015.cnblogs.com/blog/1039209/201701/1039209-20170112201726431-1637890429.png)

这里需要注意的是：

* 这个表单是根据Question模型文件自动生成的;

* 模型中不同类型的字段（DateTimeField、CharField）会对应相应的HTML输入控件。每一种类型的字段，Django管理站点都知道如何显示它们;

* 每个DateTimeField字段都会有个方便的JavaScript快捷方式。Date有个“Today”的快捷键和一个弹出式日历，time栏有个“Now”的快捷键和一个列出常用时间选项的弹出式窗口。

在页面的底部，则是一些可选项按钮：

* Save  —— 保存更改，并返回当前类型对象的变更列表界面;

* Save and add another：保存当前修改，并加载一个新的空白的当前类型对象的表单;

* Save and continue editing：保存当前修改，并重新加载该对象的编辑页面;
 
* delete：弹出一个删除确认页面

如果“Date published”字段的值和你在前面教程创建它的时候不一致，可能是你没有正确的配置TIME_ZONE，在国内，通常是8个小时的时间差别。修改TIME_ZONE配置并重新加载页面，就能显示正确的时间了

通过“Today”和“Now”这两个快捷方式来更改“Date published”字段。 然后点击 “Save and continue editing”。然后点击右上角的“History”按钮。 你将看到一个页面，列出了通过Django管理界面对此对象所做的全部更改的清单，包含有时间戳和修改人的姓名等信息：

![question4](http://images2015.cnblogs.com/blog/1039209/201701/1039209-20170112201734916-561350796.png)

到此，你对模型API和admin站点有了一定的熟悉，可以进入下一阶段的教程了。




