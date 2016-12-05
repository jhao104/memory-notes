>   在做一个可视化配置爬虫项目时，需要配置爬虫的用户自己输入xpath和csspath路径以提取数据或做浏览器操作。考虑到用户的有时会输入错误的xpath或csspath路径，后台需要对其做合法性校验。

## xpath有效性校验

对于xpath的有效性检验，使用第三方lxml模块中的etree.XPathEvalError进行校验。不得不说lxml是一个解析爬虫数据的利器，当etree.xpath()遇到不合法的xpath路径时会抛出XPathEvalError错误。

代码如下：
```
from lxml import etree
from StringIO import StringIO

def _validXpathExpression(xpath):
    """
    检查xpath合法性
    :param xpath:
    :return:
    """
    tree = etree.parse(StringIO('<foo><bar></bar></foo>'))
    try:
        tree.xpath(xpath)
        return True
    except etree.XPathEvalError, e:
        return False
```
只有当输入的xpath路径合法时返回True。
验证：
```
>>>print _validXpathExpression('./div[@class="name"]/a/text()')
>>>True
>>>
>>>print _validXpathExpression('./div(@class="name")')
>>>False
```

## csspath有效性检验

对于csspath检验的思路时，借助python标准库cssselect的css_to_xpath()方法。当输入的csspath不合法时会抛出SelectorError错误。

代码如下:
```
from cssselect.parser import SelectorError
from cssselect.xpath import HTMLTranslator

def _validCssExpression(css):
    """
    检查css合法性
    :param css:
    :return:
    """
    try:
        HTMLTranslator().css_to_xpath(css)
        return True
    except SelectorError, e:
        return False
```
只有当输入的csspath路径合法时返回True。
验证：
```
>>>print _validCssExpression('.content>a')
>>>True
>>>
>>>print _validCssExpression('.content>a[123]')
>>>False
```