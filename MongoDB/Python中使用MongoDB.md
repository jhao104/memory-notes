> Python是开发社区中用于许多不同类型应用的强大编程语言。很多人都知道它是可以处理几乎任何任务的灵活语言。因此，在Python应用中需要一个什么样的与语言本身一样灵活的数据库呢？那就是NoSQL，比如MongoDB。

> 英文原文:https://realpython.com/blog/python/introduction-to-mongodb-and-python

　　



## 1、SQL vs NoSQL

　　如果你不是很熟悉NoSQL这个概念，MongoDB就是一个NoSQL数据库。近几年来它越来越受到整个行业的欢迎。NoSQL数据库提供了一个和关系型数据库非常不同的检索方式和存储数据功能。

　　在NoSQL出现的几十年来，SQL数据库是开发者寻求构建大型、可扩展系统的唯一选择之一。然而，越来越多的需求要求存储复杂数据结构的能力。这推动了NoSQL数据库的诞生，它允许开发者存储异构和无结构的数据。

　　当到数据库方案选择时，大多数人都问自己最后一个问题，“SQL或NoSQL的？”。无论是SQL和NoSQL都有自己的长处和弱点，你应该选择适合您的应用需求中最好的之一。这里是两者之间的一些区别：

### SQL

* 模型是关系型的；

* 数据被存放在表中；

* 适用于每条记录都是相同类型并具有相同属性的情况；

* 存储规范需要预定义结构；

* 添加新的属性意味着你必须改变整体架构；

* ACID事务支持；

### NoSQL

* 模型是非关系型的;

* 可以存储Json、键值对等(决定于NoSQL数据库类型)；

* 并不是每条记录都要有相同的结构；

* 添加带有新属性的数据时，不会影响其他；

* 支持ACID事务，根据使用的NoSQL的数据库而有所不同；

* 一致性可以改变；

* 横向扩展；

　　在两种类型的数据库之间还有许多其他的区别，但上面提到的是一些更重要的区别。根据您的具体情况，使用SQL数据库可能是首选，而在其他情况下，NoSQL的是更明显的选择。当选择一个数据库时，您应该谨慎考虑每个数据库的优势和劣势。

　　NoSQL的一个好处是，有许多不同类型的数据库可供选择，并且每个都有自己的用例：

* key-value存储：[DynamoDB](https://aws.amazon.com/cn/dynamodb/)

* 文档存储：[CouchDB](http://couchdb.apache.org/)，[MongoDB](https://www.mongodb.com/)，[RethinkDB](https://www.rethinkdb.com/)

* 列存储：[Cassandra](http://cassandra.apache.org/)

* 数据结构: [Redis](https://redis.io/)，[SSDB](http://ssdb.io/zh_cn/)

　　还有很多，但这些是一些更常见的类型。近年来，SQL和NoSQL数据库甚至已经开始合并。例如，PostgreSQL现在支持存储和查询JSON数据，很像MongoDB。有了这个，你可以用Postgres实现MongoDB一样的功能，但你仍然没有MongoDB的其他优势（如横向扩容和简单的界面，等等）。

## 2、MongoDB

　　现在，让我们将视线转移到本文的重点，并阐明的MongoDB的具体的一些情况。

　　MongoDB是一个面向文档的，开源数据库程序，它平台无关。MongoDB像其他一些NoSQL数据库（但不是全部！）使用JSON结构的文档存储数据。这是使得数据非常灵活，不需要的Schema。

　　一些比较重要的特点是：

* 支持多种标准查询类型，比如matching()、comparison (, )或者正则表达式；

* 可以存储几乎任何类型的数据，无论是结构化，部分结构化，甚至是多态；

* 要扩展和处理更多查询，只需添加更多的机器；

* 它是高度灵活和敏捷，让您能够快速开发应用程序；

* 作为基于文档的数据库意味着您可以在单个文档中存储有关您的模型的所有信息；

* 您可以随时更改数据库的Schema;

* 许多关系型数据库的功能也可以在MongoDB使用（如索引）。

　　在运行方面，MongoDB中有相当多的功能在其他数据库中是没有的:


* 无论您需要独立服务器还是完整的独立服务器集群，MongoDB都可以根据需要进行扩展;

* MongoDB还通过在各个分片上自动移动数据来提供负载均衡支持；

* 它具有自动故障转移支持，如果主服务器Down掉，新的主服务器将自动启动并运行；

* MongoDB的管理服务（MMS）可以用于监控和备份MongoDB的基础设施服务；

* 不像关系数据库，由于内存映射文件，你将节省相当多的RAM。

　　虽然起初MongoDB似乎是解决我们许多问题的数据库，但它不是没有缺点的。MongoDB的一个常见缺点是缺少对ACID事务的支持，MongoDB在[特定场景下支持ACID事务](https://docs.mongodb.com/v3.4/core/write-operations-atomicity/)，但不是在所有情况。在单文档级别，支持ACID事务（这是大多数事务发生的地方）。但是，由于MongoDB的分布式性质，不支持处理多个文档的事务。

　　MongoDB还缺少对自然join查询支持。在MongoDB看来：文档意在包罗万象，这意味着，一般来说，它们不需要参考其他文档。在现实世界中，这并不总是有效的，因为我们使用的数据是关系性的。因此，许多人认为MongoDB应该被用作一个SQL数据库的补充数据库，但是当你使用MongoDB是，你会发现这是错误的。

## 3、PyMongo

　　现在我们已经描述了MongoDB的是什么，让我们来看看如何在Python中实际使用它。由MongoDB开发者发布的官方驱动程序[PyMongo](https://pypi.python.org/pypi/pymongo/)，这里通过一些例子介绍，但你也应该查看[完整的文档](https://api.mongodb.com/python/current/)，因为我们无法面面俱到。

　　当然第一件事就是安装，最简单的方式就是`pip`：
```
pip install pymongo==3.4.0
```

> 注:有关更全面的指南，请查看文档的[安装/升级](https://api.mongodb.com/python/3.4.0/installation.html)页面，并按照其中的步骤进行设置

　　完成设置后，启动的Python控制台并运行以下命令：
```
>>> import pymongo
```

　　如果没有提出任何异常就说明安装成功了

### 建立连接
 
　　使用`MongoClient`对象建立连接：

```
from pymongo import MongoClient
client = MongoClient()
```

　　使用上面的代码片段，将建立连接到默认主机（localhost）和端口（27017）。您还可以指定主机和/或使用端口：

```
client = MongoClient('localhost', 27017)
```

　　或者使用MongoURl格式：

```
client = MongoClient('mongodb://localhost:27017')
```

### 访问数据库

　　一旦你有一个连接的`MongoClient`实例，你可以在Mongo服务器中访问任何数据库。如果要访问一个数据库，你可以当作属性一样访问：
```
db = client.pymongo_test
```

　　或者你也可以使用字典形式的访问：
```
db = client['pymongo_test']
```

　　如果您的指定数据库已创建，实际上并不重要。通过指定此数据库名称并将数据保存到其中，您将自动创建数据库。

### 插入文档

　　在数据库中存储数据，就如同调用只是两行代码一样容易。第一行指定你将使用哪个集合。在MongoDB中术语中，一个集合是在数据库中存储在一起的一组文档(相当于SQL的表)。集合和文档类似于SQL表和行。第二行是使用集合插入数据insert_one()的方法：

```
posts = db.posts
post_data = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
result = posts.insert_one(post_data)
print('One post: {0}'.format(result.inserted_id))
```


　　我们甚至可以使用insert_one()同时插入很多文档，如果你有很多的文档添加到数据库中，可以使用方法insert_many()。此方法接受一个list参数：

```
post_1 = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
post_2 = {
    'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'
}
post_3 = {
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    'author': 'Bill'
}
new_result = posts.insert_many([post_1, post_2, post_3])
print('Multiple posts: {0}'.format(new_result.inserted_ids))
```

　　你应该看到类似输出：
```
One post: 584d947dea542a13e9ec7ae6
Multiple posts: [
    ObjectId('584d947dea542a13e9ec7ae7'),
    ObjectId('584d947dea542a13e9ec7ae8'),
    ObjectId('584d947dea542a13e9ec7ae9')
]
```

> 注意: 不要担心，你和上面显示不一样。它们是在插入数据时，由Unix的纪元，机器标识符和其他唯一数据组成的动态标识。

### 检索文档

　　检索文档可以使用find_one()方法，比如要找到author为Bill的记录:

```
bills_post = posts.find_one({'author': 'Bill'})
print(bills_post)

运行结果:
{
    'author': 'Bill',
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    '_id': ObjectId('584c4afdea542a766d254241')
}
```

　　您可能已经注意到，这篇文章的ObjectId是设置的_id，这是以后可以使用唯一标识。如果需要查询多条记录可以使用find()方法：

```
scotts_posts = posts.find({'author': 'Scott'})
print(scotts_posts)

结果:
<pymongo.cursor.Cursor object at 0x109852f98>

```
　　他的主要区别在于文档数据不是作为数组直接返回给我们。相反，我们得到一个游标对象的实例。这Cursor是一个包含相当多的辅助方法，以帮助您处理数据的迭代对象。要获得每个文档，只需遍历结果：

```
for post in scotts_posts:
    print(post)
```

### 4、MongoEngine

　　虽然PyMongo是非常容易使用，总体上是一个伟大的轮子，但是许多项目使用它都可能太低水平。简而言之，你必须编写很多自己的代码来持续地保存，检索和删除对象。PyMongo之上提供了一个更高的抽象一个库是MongoEngine。MongoEngine是一个对象文档映射器（ODM），它大致相当于一个基于SQL的对象关系映射器（ORM）。MongoEngine提供的抽象是基于类的，所以你创建的所有模型都是类。虽然有相当多的Python的库可以帮助您使用MongoDB，MongoEngine是一个更好的，因为它有一个很好的组合的功能，灵活性和社区支持。


　　使用pip安装:
```
pip install mongoengine==0.10.7
```

　　连接:
```
from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)
```
　　
　　和pymongo不同。MongoEngine需要制定数据库名称。

#### 定义文档

　　建立文档之前，需要定义文档中要存放数据的字段。与许多其他ORM类似，我们将通过继承Document类，并提供我们想要的数据类型来做到这一点：

````
import datetime

class Post(Document):
    title = StringField(required=True, max_length=200)
    content = StringField(required=True)
    author = StringField(required=True, max_length=50)
    published = DateTimeField(default=datetime.datetime.now)
````

　　在这个简单的模型中，我们已经告诉MongoEngine，我们的Post实例有title、content、author、published。现在Document对象可以使用该信息来验证我们提供它的数据。

　　因此，如果我们试图保存Post的中没有title那么它会抛出一个Exception，让我们知道。我们甚至可以进一步利用这个并添加更多的限制：

* required：设置必须；

* default：如果没有其他值给出使用指定的默认值

* unique：确保集合中没有其他document有此字段的值相同

* choices：确保该字段的值等于数组中的给定值之一

#### 保存文档

　　将文档保存到数据库中，我们将使用save()的方法。如果文档中的数据库已经存在，则所有的更改将在原子水平上对现有的文档进行。如果它不存在，但是，那么它会被创建。

　　这里是创建和保存一个文档的例子：

```
post_1 = Post(
    title='Sample Post',
    content='Some engaging content',
    author='Scott'
)
post_1.save()       # This will perform an insert
print(post_1.title)
post_1.title = 'A Better Post Title'
post_1.save()       # This will perform an atomic edit on "title"
print(post_1.title)
```

　　调用save()的时候需要注意几点:

* PyMongo将在您调用.save（）时执行验证，这意味着它将根据您在类中声明的模式检查要保存的数据，如果违反模式（或约束），则抛出异常并且不保存数据；

* 由于Mongo不支持真正的事务，因此没有办法像在SQL数据库中那样“回滚”.save（）调用。

　　当你保存的数据没有title时:

```
post_2 = Post(content='Content goes here', author='Michael')
post_2.save()


raise ValidationError(message, errors=errors)
mongoengine.errors.ValidationError:
ValidationError (Post:None) (Field is required: ['title'])
```


#### 向对象的特性

　　使用MongoEngine是面向对象的，你也可以添加方法到你的子类文档。例如下面的示例，其中函数用于修改默认查询集（返回集合的所有对象）。通过使用它，我们可以对类应用默认过滤器，并只获取所需的对象

```
class Post(Document):
    title = StringField()
    published = BooleanField()

    @queryset_manager
    def live_posts(clazz, queryset):
        return queryset.filter(published=True)

```

#### 关联其他文档

　　您还可以使用ReferenceField对象来创建从一个文档到另一个文档的引用。MongoEngine在访问时自动惰性处理引用。

```
class Author(Document):
    name = StringField()

class Post(Document):
    author = ReferenceField(Author)

Post.objects.first().author.name
```

　　在上面的代码中，使用文档"外键"，我们可以很容易地找到第一篇文章的作者。其实还有比这里介绍的更多的字段类（和参数），所以一定要查看[文档字段](http://docs.mongoengine.org/apireference.html#fields)更多信息。
　　
   从所有这些示例中，您应该能够看到，MongoEngine非常适合管理几乎任何类型的应用程序的数据库对象。这些功能使得创建一个高效可扩展程序变得非常容易。如果你正在寻找更多关于MongoEngine的帮助，请务必查阅他们的[用户指南](http://docs.mongoengine.org/guide/index.html)。
   
   
