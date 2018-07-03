## 装饰器作用

[decorator](https://docs.djangoproject.com/en/2.0/topics/http/decorators/)是当今最流行的设计模式之一，很多使用它的人并不知道它是一种设计模式。这种模式有什么特别之处? 有兴趣可以看看[Python Wiki](https://wiki.python.org/moin/DecoratorPattern)上例子，使用它可以很方便地修改对象行为，通过使用类似例中的接口将修改动作封装在装饰对象中。

**decorator** 可以动态地修改函数、方法或类的功能，而无需创建子类或修改类的源代码。正因为如此，装饰器可以让代码将变得**更干净**、**更可读**、**更可维护**(这很重要!)，并且减少了许多冗余但又不得不写的代码，使我们可以使用单个方法向多个类添加功能。

对于装饰器的重用性和易用性，Django里面的[@login_required](https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-login-required-decorator)就是一个很好的例子。使用它只用一句代码就可以检查用户是否通过身份验证，并将未登录用户重定向到登录url。

该装饰器的使用方法如下:
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def my_view(request):
    ...
```

每次用户试图访问 `my_view` 时，都会进入 `login_required` 中的代码。

## Django装饰器

下面介绍一些个人认为比较有用的，或者是之前使用过的具有积极效果的装饰器。事先声明，如要实现同样的业务场景，并不是只有本文中的方法。Django可以实现各种各样的装饰器，这完全根据您的需要进行定制。

### Group Required

有时需要保护一些视图，只允许某些用户组访问。这时就可以使用下面的装饰器来检查用户是否属于该用户组。
```python
from django.contrib.auth.decorators import user_passes_test


def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):
       if u.is_authenticated():
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)


# The way to use this decorator is:
@group_required('admins', 'seller')
def my_view(request, pk):
    ...
```

有关此装饰器更多的介绍，可以参考[这里](https://djangosnippets.org/snippets/1703/)。

### Anonymous required

这个装饰器是参考Django自带的 `login_required` 装饰器，但是功能是相反的情况，即用户必须是未登录的，否则用户将被重定向到 `settings.py` 中定义的地址。当我们想要已登录的用户不允许进入某些视图(比如登录)时，非常有用。
```python
def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous(),
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator


# The way to use this decorator is:
@anonymous_required
def my_view(request, pk):
    ...
```

有关此装饰器更多的介绍，可以参考[这里](https://djangosnippets.org/snippets/2969/)。

### Superuser required

这个装饰器和上面的 `group_required` 类似， 但是它只允许超级用户才能访问视图。
```python
from django.core.exceptions import PermissionDenied


def superuser_only(function):
    """Limit view to superusers only."""

    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)

    return _inner


# The way to use this decorator is:
@superuser_only
def my_view(request):
    ...
```

有关此装饰器更多的介绍，可以参考[这里](https://djangosnippets.org/snippets/1575/)。

### Ajax required

这个装饰器用于检查请求是否是AJAX请求，在使用jQuery等Javascript框架时，这是一个非常有用的装饰器，也是一种保护应用程序的好方法。

```python
from django.http import HttpResponseBadRequest


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:
 
    @ajax_required
    def my_view(request):
        ....
 
    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


# The way to use this decorator is:
@ajax_required
def my_view(request):
    ...
```

有关此装饰器更多的介绍，可以参考[这里](https://djangosnippets.org/snippets/771/)。

### Time it

如果您需要改进某个视图的响应时间，或者只想知道运行需要多长时间，那么这个装饰器非常有用。

```python
def timeit(method):

   def timed(*args, **kw):
       ts = time.time()
       result = method(*args, **kw)
       te = time.time()
       print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te - ts))
       return result

   return timed


# The way to use this decorator is:
@timeit
def my_view(request):
    ...
```

有关此装饰器更多的介绍，可以参考[这里](https://www.zopyx.com/andreas-jung/contents/a-python-decorator-for-measuring-the-execution-time-of-methods)。

### 自定义功能

下面这个装饰器只是一个示例，测试你能够轻松地检查某些权限或某些判断条件，并100%自己定制。
想象你有一个博客、购物论坛，如果用户需要有很多积分才能发表评论，这是一个避免垃圾信息的好方法。下面创建一个装饰器来检查用户是否已登录并拥有超过10个积分，这样才可以发表评论，否则将抛出一个Forbidden。

```python
from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)


def user_can_write_a_review(func):
   """View decorator that checks a user is allowed to write a review, in negative case the decorator return Forbidden"""

   @functools.wraps(func)
   def wrapper(request, *args, **kwargs):
       if request.user.is_authenticated() and request.user.points < 10:
           logger.warning('The {} user has tried to write a review, but does not have enough points to do so'.format( request.user.pk))
           return HttpResponseForbidden()

       return func(request, *args, **kwargs)

   return wrapper
```
