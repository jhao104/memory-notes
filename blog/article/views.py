# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     views.py  
   Description :  
   Author :       JHao
   date：          2016/11/18
-------------------------------------------------
   Change Activity:
                   2016/11/18: 
-------------------------------------------------
"""

# -*- coding: UTF-8 -*-

from django.shortcuts import render, get_object_or_404, redirect, render_to_response
# from django.http import Http404, HttpResponse

from article.models import Article


# Create your views here.

def home(request):
    post_list = Article.objects.all()  # 获取全部文章
    return render(request, 'article/articles.html', {"post_list": post_list,
                                                     "title": "j_hao104's blog"})


def detail(request, id):
    post = get_object_or_404(Article, pk=id)
    post.viewed()
    return render(request, 'article/article.html', {"post": post,
                                                    "title": post.title})


def category(request, id):
    post_list = Article.objects.filter(category_id=id)
    return render(request, 'article/articles.html', {"post_list": post_list,
                                                     "title": "j_hao104's blog"})


def archives_i(request):
    return render(request, 'article/archives_i.html')


def archives(request):
    return render(request, 'article/archives.html')
