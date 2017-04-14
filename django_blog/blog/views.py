# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render, get_object_or_404
from blog.models import Article, Category


def Index(request):
    """
    博客首页
    :param request:
    :return:
    """
    article_list = Article.objects.all().order_by('date_time')
    if len(article_list) > 7:
        article_list = article_list[0:7]
    return render(request, 'blog/index.html', {"html_title": u"博客首页",
                                               "article_list": article_list,
                                               "source_id": "index"})


def Articles(request, pk):
    """
    博客列表页面
    :param request:
    :param pk:
    :return:
    """
    pk = int(pk)
    if pk:
        category_object = get_object_or_404(Category, pk=pk)
        category = category_object.name
        article_list = Article.objects.filter(category_id=pk)
    else:
        # pk为0时表示全部
        article_list = Article.objects.all()  # 获取全部文章
        category = u''
    return render(request, 'blog/articles.html', {"article_list": article_list,
                                                  "category": category,
                                                  "html_title": "博客"})


def About(request):
    return render(request, 'blog/about.html')


def Archive(request):
    return render(request, 'blog/articles.html')


def Link(request):
    return render(request, 'blog/link.html')
