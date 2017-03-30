>本教程接[Part3](https://github.com/jhao104/memory-notes/blob/master/Django/Django%201.10%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3-%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%BA%94%E7%94%A8Part3-%E8%A7%86%E5%9B%BE%E5%92%8C%E6%A8%A1%E6%9D%BF.md)开始。继续网页投票应用程序，并将重点介绍简单的表单处理和精简代码。

## 一个简单表单

　　更新一下在上一个教程中编写的投票详细页面的模板`polls/detail.html`，让它包含一个`HTML<form>` 元素：
```html
# polls/templates/polls/detail.html

<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Vote" />
</form>
```

　　关于上面的代码:

* 在模板中Question的每个Choice都有一个单选按钮用于选择。每个单选按钮的value属性是对应的各个Choice的ID。每个单选按钮的name是"choice"。这意味着，当有人选择一个单选按钮并提交表单提交时，它将发送一个POST数据choice=#，其中# 为选择的Choice的ID。这是HTML表单的基本概念;

* action表示你要发送的目的url，method表示提交数据的方式;

* forloop.counter表示for循环的次数;

* 由于我们发送了一个POST请求，就必须考虑一个跨站请求伪造的问题，简称CSRF（具体含义请百度）。Django为你提供了一个简单的方法来避免这个困扰，那就是在form表单内添加一条{% csrf_token %}标签，标签名不可更改，固定格式，位置任意，只要是在form表单内。

　　现在，创建一个Django视图来处理提交的数据，在Part3中已经创建了一个URLconf ，包含这一行:

```python
# polls/urls.py

url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
```

　　修改vote()函数。 将下面的代码添加到polls/views.py:

```python
# polls/views.py
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Choice, Question
# ...
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 出现异常重新显示投票表单
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 成功处理数据后，自动跳转到结果页面，防止用户连续多次提交。
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
```

　　上面代码里有些东西需要解释:

* request.POST是一个类似字典的对象，允许你通过键名访问提交的数据。代码中`request.POST['choice']`返回被选择Choice的ID，并且值的类型永远是string字符串;

* 如果在POST数据中没有提供choice，`request.POST['choice']`将引发一个KeyError。上面的`try ... except`就是用来检查KeyError，如果没有给出choice将重新显示Question表单和错误信息;

* 在将Choice得票数加1之后，返回一个HttpResponseRedirect而不是常用的HttpResponse。HttpResponseRedirect只接收一个参数：用户将要被重定向的URL;

* 在这个例子中，HttpResponseRedirect的构造函数中使用reverse()函数。这个函数可以避免在视图函数中硬编码URL。它需要我们给出想要跳转的视图的名字和该视图所对应的URL模式中需要给该视图提供的参数。 在本例中，使用在Part3中设定的URLconf，reverse()调用将返回一个这样的字符串：`'/polls/3/results/'`。

　　当对Question进行投票后，vote()视图将请求重定向到Question的结果界面。下面来编写这个视图：

```python
#polls/views.py

from django.shortcuts import get_object_or_404, render


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
```

　　这和detail()视图几乎一模一样。唯一的不同是模板的名字。稍后再来优化这个问题。下面创建一个polls/results.html模板：

```html
# polls/templates/polls/results.html

<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```

　　现在，在浏览器中访问/polls/1/然后为Question投票。应该看到一个投票结果页面，并且在每次投票后都会更新。 如果提交时没有选择任何Choice，应该会看到错误信息。

>注: views()视图的代码确实有一个小问题。它首先从数据库中获取selected_choice对象，计算新的投票数值然后将其保写回数据库。如果您的网站的两位用户尝试在完全相同的时间投票，这可能会出错。这被称为竞争条件。如果您有兴趣，可以阅读[使用F()避免竞争条件](https://docs.djangoproject.com/en/1.10/ref/models/expressions/#avoiding-race-conditions-using-f)，以了解如何解决此问题;

## 使用通用视图:减少代码冗余

　　上面的detail、index和results视图的代码非常相似，有点冗余，这是一个程序猿不能忍受的。他们都具有类似的业务逻辑，实现类似的功能：通过从URL传递过来的参数去数据库查询数据，加载一个模板，利用刚才的数据渲染模板，返回这个模板。由于这个过程是如此的常见，Django又很善解人意的帮你想办法偷懒了，它提供了一种快捷方式，名为`generic views`系统。

　　Generic views会将常见的模式抽象化，可以使你在编写app时甚至不需要编写Python代码。

　　下面将投票应用转换成使用通用视图系统，这样可以删除许多冗余的代码。仅仅需要做以下几步来完成转换：

* 修改URLconf;

* 删除一些旧的无用的视图;

* 采用基于通用视图的新视图。

## 改进URLconf

```python
# polls/urls.py

from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

```

　　注意在第二个和第三个模式的正则表达式中，匹配的模式的名字由`<question_id>` 变成 `<pk>`

## 改进视图

　　下面将删除旧的index、detail和 results 视图，并用Django的通用视图代替:

```python
# polls/views.py

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    ... # same as above, no changes needed.
```

　　这里使用两个通用视图：[ListView](https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/#django.views.generic.list.ListView)和[DetailView](https://docs.djangoproject.com/en/1.10/ref/class-based-views/generic-display/#django.views.generic.list.ListView)。这两个视图分别代表“显示对象列表”和“显示特定类型对象的详细信息页面”的抽象概念。

* 每个通用视图需要知道它将作用于哪个模型。 这由model 属性提供;

* DetailView都是从URL中捕获名为"pk"的主键值，因此才需要把polls/urls.py中question_id改成了pk以使通用视图可以找到主键值。
 
　　默认情况下，DetailView泛型视图使用一个称作`<app name>/<model name>_detail.html`的模板。在本例中，实际使用的是`polls/question_detail.html`。template_name属性就是用来指定这个模板名的，用于代替自动生成的默认模板名。

　　在教程的前面部分，我们给模板提供了一个包含question和latest_question_list的上下文变量。而对于DetailView，question变量会被自动提供，因为我们使用了Django的模型（Question），Django会智能的选择合适的上下文变量。然而，对于ListView，自动生成的上下文变量是question_list。为了覆盖它，我们提供了context_object_name属性，指定说我们希望使用latest_question_list而不是question_list。

　　现在你可以运行开发服务器，然后试试基于泛型视图的应用程序了。

　　更多关于通用视图的详细信息，请查看[通用视图文档](https://docs.djangoproject.com/en/1.10/topics/class-based-views/)。