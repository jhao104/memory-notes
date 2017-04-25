
　　本教程上接教程[Part4](https://github.com/jhao104/memory-notes/blob/master/Django/Django%201.10%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3-%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%BA%94%E7%94%A8Part4-%E8%A1%A8%E5%8D%95%E5%92%8C%E9%80%9A%E7%94%A8%E8%A7%86%E5%9B%BE.md)。 前面已经建立一个网页投票应用，现在将为它创建一些自动化测试。

## 自动化测试简介

### 什么是自动化测试

　　测试是检查你的代码是否正常运行的行为。测试也分为不同的级别。有些测试可能是用于某个细节操作（比如特定的模型方法是否返回预期的值），而有些测试是检查软件的整体操作（比如站点上的一系列用户输入是否产生所需的结果）。这和[Part2](https://github.com/jhao104/django-chinese-docs-1.10/blob/master/intro/tutorial02/%E5%BC%80%E5%8F%91%E7%AC%AC%E4%B8%80%E4%B8%AADjango%E5%BA%94%E7%94%A8%2CPart2.md)中的测试是一样的，使用shell来检查方法的行为，或者运行应用程序并输入数据来检查它的行为。

　　自动化测试的不同之处就在于这些测试会由系统来帮你完成。你只需要创建一组测试一次，即便以后对应用进行了更改，您仍可以使用这组测试代码检查应用是否按照预期的方式工作，而无需执行耗时的手动测试。

### 为什么需要自动化测试

　　那么为什么现在要自动化测试？你可能感觉学习Python/Django已经足够，再去学习其他的东西也许需要付出巨大的努力而且没有必要，毕竟我们的投票应用已经愉快地运行起来了。与其花时间去做自动化测试还不如改进现在的应用。如果你学习Django就是仅仅是为了创建一个小小投票应用，那么涉足自动化测试显然没有必要。 但如果不是这样，现在是一个很好的学习机会。

* 测试可以节约开发时间

　　某种程度上，“检查并发现工作正常”似乎是种比较满意的测试结果。但在一些复杂的应用中，你会发现组件之间存在各种各样复杂的交互关系。

　　这些组件有任何小的的更改都有可能会对应用程序的行为产生意想不到的后果。要得出“似乎工作正常”的结果，可能意味着你需要使用二十种不同的测试数据来测试你的代码，而这仅仅是为了确保你没有做错某些事，这种方法效率低下。然而，自动化测试只需要数秒就可以完成以上的任务。如果出现了错误，还能够帮助找出引发这个异常行为的代码。

　　有时候你可能会觉得编写测试程序相比起有价值的、创造性的编程工作显得单调乏味、无趣，尤其是当你的代码工作正常时。但是，比起用几个小时的时间来手动测试你的程序，或者试图找出代码中一个新生问题的原因，编写自动化测试程序的性价比还是很高的。

* 测试可以发现并防止问题

　　将测试看做只是开发中消极的一面是错误的，没有测试，应用程序的目的或预期行为可能是相当不透明的。即使这是你自己的代码，你也会发现自己正在都不知道它在做什么。测试可以改变这一情况； 它们使你的代码内部变得明晰，当错误出现后，它们会明确地指出哪部分代码出了问题——甚至你自己都不会料到问题会出现在那里。

* 测试使您的代码更受欢迎

　　你可能已经创建了一个堪称辉煌的软件，但是你会发现许多其他的开发者会由于它缺少测试程序而拒绝查看它一眼；没有测试程序，他们不会信任它。 Jacob Kaplan-Moss，Django最初的几个开发者之一，说过“不具有测试程序的代码是设计上的错误”。你需要开始编写测试的另一个原因就是其他的开发者在他们认真研读你的代码前可能想要查看一下它有没有测试。

* 测试有助于团队合作

　　之前的观点是从单个开发人员来维护一个程序这个方向来阐述的。 复杂的应用将会被一个团队来维护。 测试能够减少同事在无意间破坏你的代码的情况（和你在不知情的情况下破坏别人的代码的情况）。 如果你想在团队中做一个好的Django开发者，你必须擅长测试！

##  基本的测试策略

　　编写测试程序有很多种方法。一些程序员遵循一种叫做“[测试驱动开发](https://en.wikipedia.org/wiki/Test-driven_development)”的规则，他们在编写代码前会先编好测试程序。看起来似乎有点反人类，但实际上这种方法与大多数人经常的做法很相似：先描述一个问题，然后编写代码来解决这个问题。测试驱动开发可以简单地用Python测试用例将问题格式化。

　　很多时候，刚接触测试的人会先编写一些代码后才编写测试程序。事实上，在之前就编写一些测试会好一点，但不管怎么说什么时候开始都不算晚。

　　有时候你很难决定从什么时候开始编写测试。如果你已经编写了数千行Python代码，挑选它们中的一些来进行测试是不太容易的。这种情况下，在下次你对代码进行变更，添加一个新功能或者修复一个bug之时，编写你的第一个测试，效果会非常好。下面，让我们来编写一个测试。

## 编写第一个测试

### 发现bug

　　很巧，在我们的投票应用中有一个小bug需要修改：在Question.was_published_recently()方法的返回值中，当Qeustion在最近的一天发布的时候返回True（这是正确的），然而当Question在未来的日期内发布的时候也返回True（这是错误的）。

　　要检查该bug是否真的存在，使用Admin创建一个未来的日期，并使用shell检查：
```shell
>>>python manage.py shell

In [1]: import datetime
In [2]: from django.utils import timezone
In [3]: from polls.models import Question
# 创建一个pub_date在30天之后的Question实例
In [4]: future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
# 检查was_published_recently返回值
In [5]: future_question.was_published_recently()
Out[5]: True
```

　　由于“将来”不等于“最近”，因此这显然是个bug。

### 创建一个测试来暴露这个bug

　　刚才我们是在shell中测试了这个bug，那如何通过自动化测试来发现这个bug呢？

　　通常，我们会把测试代码放在应用的tests.py文件中；测试系统将自动地从任何名字以test开头的文件中查找测试程序。

　　将下面的代码输入投票应用的tests.py文件中：
```python

# polls/tests.py

import datetime

from django.utils import timezone
from django.test import TestCase
from .models import Question


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        在未来发布的问卷应该返回False
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```
　　我们在这里创建了一个`django.test.TestCase`的子类，它具有一个方法，该方法创建一个`pub_date`在未来的`Question`实例。最后我们检查`was_published_recently()`的输出，它应该是 False。

### 运行测试程序

　　在终端中，运行下面的命令：
```shell
python manage.py test polls
```

　　你将看到结果如下：
```shell
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_was_published_recently_with_future_question (polls.tests.QuestionMethodTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/path/to/mysite/polls/tests.py", line 16, in test_was_published_recently_with_future_question
    self.assertIs(future_question.was_published_recently(), False)
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

　　这背后的过程：

* `python manage.py test polls`命令会查找所有polls应用中的测试程序

* 发现一个`django.test.TestCase`的子类

* 它为测试创建了一个特定的数据库

* 查找函数名以test开头的测试方法

* 在`test_was_published_recently_with_future_question`方法中，创建一个`Question`实例，该实例的`pub_data`字段的值是30天后的未来日期

* 然后利用`assertIs()`方法，它发现`was_published_recently()`返回了True，而不是我们希望的False

　　这个测试通知我们哪个测试失败了，错误出现在哪一行。

### 修复bug

　　现在我们已经知道问题是什么：如果它的`pub_date`是在未来，`Question.was_published_recently()`应该返回False。在models.py中修复这个方法，让它只有当日期是在过去时才返回True：

```python

# polls/models.py

def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
```

　　重新运行测试：
```shell
Creating test database for alias 'default'...
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...
```

　　在找出一个bug之后，编写一个测试来验证这个错误，然后在代码中更正这个错误让我们的测试通过。未来，在应用中可能会出许多其它未知的错误，但是我们可以保证不会无意中再次引入这个错误，因为简单地运行一下这个测试就会立即提醒我们。 我们可以认为这个应用的这一小部分会永远安全了。

### 更全面的测试

　　我们可以使`was_published_recently()`方法更加可靠，事实上，在修复一个错误的同时又引入一个新的错误将是一件很令人尴尬的事。下面，我们在同一个测试类中再额外添加两个其它的方法，来更加全面地进行测试：

```python
# polls/tests.py

def test_was_published_recently_with_old_question(self):
    """
    日期超过1天的将返回False。这里创建了一个30天前发布的实例。
    """
    time = timezone.now() - datetime.timedelta(days=30)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)
    
    
def test_was_published_recently_with_recent_question(self):
    """
    最近一天内的将返回True。这里创建了一个1小时内发布的实例。
    """
    time = timezone.now() - datetime.timedelta(hours=1)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)
```

　　现在我们有三个测试来保证无论发布时间是在过去、现在还是未来`Question.was_published_recently()`都将返回正确的结果。最后，polls应用虽然简单，但是无论它今后会变得多么复杂以及会和多少其它的应用产生相互作用，我们都能保证`Question.was_published_recently()`会按照预期的那样工作。

## 测试视图

　　这个投票应用没有辨别能力：它将会发布任何的Question，包括`pub_date`字段是未来的。我们应该改进这一点。让`pub_date`是将来时间的Question应该在未来发布，但是一直不可见，直到那个时间点才会变得可见。

### 什么是视图测试

　　当我们修复上面的错误时，我们先写测试，然后修改代码来修复它。 事实上，这是测试驱动开发的一个简单的例子，但做的顺序并不真的重要。在我们的第一个测试中，我们专注于代码内部的行为。 在这个测试中，我们想要通过浏览器从用户的角度来检查它的行为。在我们试着修复任何事情之前，让我们先查看一下我们能用到的工具。

### Django的测试客户端

　　Django提供了一个测试客户端用来模拟用户和代码的交互。我们可以在`tests.py`甚至`shell`中使用它。先介绍使用`shell`的情况，这种方式下，需要做很多在tests.py中不必做的事。首先是设置测试环境：

```shell
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
```

　　`setup_test_environment()`会安装一个模板渲染器，它使我们可以检查一些额外的属性比如`response.context`，这些属性通常情况下是访问不到的。请注意，这种方法不会建立一个测试数据库，所以以下命令将运行在现有的数据库上，输出的内容也会根据你已经创建的Question的不同而稍有不同。如果你当前`settings.py`中的的`TIME_ZONE`不正确，那么你或许得不到预期的结果。在进行下一步之前，请确保时区设置正确。

　　下面我们需要导入测试客户端类（在之后的tests.py中，我们将使用django.test.TestCase类，它具有自己的客户端，不需要导入这个类）：

```shell
>>> from django.test import Client
>>> # 创建一个Client实例
>>> client = Client()
```

　　下面是具体的一些使用操作：
```shell
>>> # 从'/'获取响应
>>> response = client.get('/')
>>> # 这个地址应该返回的是404页面
>>> response.status_code
404
>>> # 另一方面我们希望在'/polls/'获取一些内容
>>> # 通过使用'reverse()'方法，而不是URL硬编码
>>> from django.urls import reverse
>>> response = client.get(reverse('polls:index'))
>>> response.status_code
200
>>> response.content
b'\n <ul>\n \n <li><a href="/polls/1/">What&#39;s up?</a></li>\n \n </ul>\n\n'
>>> # 如果下面的操作没有正常执行，有可能是你前面忘了安装测试环境--setup_test_environment() 
>>> response.context['latest_question_list']
<QuerySet [<Question: What's up?>]>
```

### 改进视图

　　投票的列表会显示还没有发布的问卷（即`pub_date`在未来的问卷）。让我们来修复它。在[Part4](https://github.com/jhao104/django-chinese-docs-1.10/blob/master/intro/tutorial04/%E7%AC%AC%E4%B8%80%E4%B8%AADjango%E5%BA%94%E7%94%A8%2CPart4.md)中，我们介绍了一个继承`ListView`的基类视图：

```python

# polls/views.py

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
```

　　我们需要在`get_queryset()`方法中对比`timezone.now()`。首先导入`timezone`模块，然后修改get_queryset()方法，如下：
```python

# polls/views.py

from django.utils import timezone

def get_queryset(self):
    """
    返回最近5个发布的Question但不包括未来的
    """
    return Question.objects.filter(
    pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
```

　　`Question.objects.filter(pub_date__lte=timezone.now())`返回一个查询集，包含`pub_date`小于等于`timezone.now`的Question。

### 测试新视图

　　现在，您可以通过启动运行服务器，在浏览器中加载站点，创建过去和将来的日期的问题，并检查仅列出已发布的站点，从而满足您的需求。如果你不想每次修改可能与这相关的代码时都重复这样做———所以我们还要根据上面的shell会话创建一个测试。将下面的代码添加到polls/tests.py：
```python

# polls/tests.py

from django.core.urlresolvers import reverse

def create_question(question_text, days):
    """
    2个参数，一个是问卷的文本内容，另外一个是当前时间的偏移天数，负值表示发布日期在过去，正值表示发布日期在将来。
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
    
class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        如果问卷不存在，给出相应的提示。
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        发布日期在过去的问卷将在index页面显示。
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question.>']
        )
        
    def test_index_view_with_a_future_question(self):
        """
        发布日期在将来的问卷不会在index页面显示
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        即使同时存在过去和将来的问卷，也只有过去的问卷会被显示。
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        index页面可以同时显示多个问卷。
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
        response.context['latest_question_list'],
        ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
```

　　让我们更详细地看下以上这些内容。

　　第一个是Question的快捷函数`create_question`，功能是将创建Question的过程封装起来。

　　`test_index_view_with_no_questions`不创建任何Question，但会检查消息“No polls are available.” 并验证`latest_question_list`为空。注意`django.test.TestCase`类提供一些额外的断言方法。在这些例子中，我们使用了`assertContains()`和`assertQuerysetEqual()`。

　　在`test_index_view_with_a_past_question`中，我们创建一个Question并验证它是否出现在列表中。

　　在`test_index_view_with_a_future_question`中，我们创建一个`pub_date`在未来的Question。数据库会为每一个测试方法进行重置，所以第一个Question已经不在那里，因此index页面里不应该有任何Question。

　　诸如此类，事实上，我们是在用测试，模拟站点上的管理员输入和用户体验，检查系统的每一个状态变化，发布的是预期的结果。

### 测试DetailView

　　然而，即使未来发布的Question不会出现在index中，如果用户知道或者猜出正确的URL依然可以访问它们。所以我们需要给DetailView视图添加一个这样的约束：

```python

# polls/views.py

class DetailView(generic.DetailView):
    ...
    def get_queryset(self):
        """
        确认Question不是在未来发布的.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
```

　　同样，我们将增加一些测试来检验pub_date在过去的Question可以显示出来，而pub_date在未来的不可以
```python

# polls/tests.py

class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        访问发布时间在将来的detail页面将返回404.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        访问发布时间在过去的detail页面将返回详细问卷内容。
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
```

### 其他测试思路

　　我们应该添加一个类似get_queryset的方法到ResultsView并为该视图创建一个新的类。这将与我们上面的范例非常类似，实际上也有许多重复。

　　还可以在其它方面改进我们的应用，并随之不断地增加测试。例如，发布一个没有Choices的Questions就显得极不合理。所以，我们的视图应该检查这点并排除这些Questions。我们的测试会创建一个不带Choices的Question然后测试它不会发布出来，同时创建一个类似的带有Choices的Question并确保它会发布出来。

　　也许登陆的管理员用户应该被允许查看还没发布的Questions，但普通访问者则不行。最重要的是：无论添加什么代码来完成这个要求，都需要提供相应的测试代码，不管你是先编写测试程序然后让这些代码通过测试，还是先用代码解决其中的逻辑再编写测试程序来检验它。

　　从某种程度上来说，你一定会查看你的测试代码，然后想知道你的测试程序是否过于臃肿，我们接着看下面的内容：

## 测试越多越好

　　看起来我们的测试代码正在逐渐失去控制。以这样的速度，测试的代码量将很快超过我们的实际应用程序代码量，对比其它简洁优雅的代码，测试代码既重复又毫无美感。没关系！随它去！大多数情况下，你可以完一个测试程序，然后忘了它。当你继续开发你的程序时，它将始终执行有效的测试功能。有时，测试程序需要更新。假设我们让只有具有Choices的Questions才会发布，在这种情况下，许多已经存在的测试都将失败：这会告诉我们哪些测试需要被修改，使得它们保持最新，所以从某种程度上讲，测试可以自己测试自己。在最坏的情况下，在你的开发过程中，你会发现许多测试变得多余。其实，这不是问题，对测试来说，冗余是一件好事。只要你的测试被合理地组织，它们就不会变得难以管理。 从经验上来说，好的做法是：

* 为每个模型或视图创建一个专属的TestClass

* 为你想测试的每一种情况建立一个单独的测试方法

* 为测试方法命名时最好从字面上能大概看出它们的功能

## 进一步测试

　　本教程仅介绍一些测试的基础知识。其实还有很多工作可以做，还有一些非常有用的工具可用于实现一些非常聪明的事情。例如，虽然我们的测试覆盖了模型的内部逻辑和视图发布信息的方式，但你还可以使用一个“基于浏览器”的框架例如[Selenium](http://www.seleniumhq.org/)来测试你的HTML文件真实渲染的样子。这些工具不仅可以让你检查你的Django代码的行为，还能够检查JavaScript的行为。它会启动一个浏览器，与你的网站进行交互，就像有一个人在操纵一样！Django包含一个[LiveServerTestCase](https://docs.djangoproject.com/en/1.10/topics/testing/tools/#django.test.LiveServerTestCase)来帮助与Selenium 这样的工具集成。

　　如果你有一个复杂的应用，你可能为了实现[持续集成](https://en.wikipedia.org/wiki/Continuous_integration)，想在每次提交代码前对代码进行自动化测试，让代码自动至少是部分自动地来控制它的质量。

　　发现你应用中未经测试的代码的一个好方法是检查测试代码的覆盖率。 这也有助于识别脆弱的甚至死代码。 如果你不能测试一段代码，这通常意味着这些代码需要被重构或者移除。 Coverage将帮助我们识别死代码。 查看[Integration with coverage.py](https://docs.djangoproject.com/en/1.10/topics/testing/advanced/#topics-testing-code-coverage)来了解更多细节。

　　[Testing in Django](https://docs.djangoproject.com/en/1.10/topics/testing/)有关于测试更加全面的信息。

## 下一步

　　关于测试的完整细节，请查看[Testing in Django](https://docs.djangoproject.com/en/1.10/topics/testing/)。

　　当你对Django 视图的测试感到满意后，请阅读本教程的[第6部分](https://docs.djangoproject.com/en/1.10/intro/tutorial06/)来了解静态文件的管理。