# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     context_processors.py  
   Description :  
   Author :       JHao
   date：          2017/4/14
-------------------------------------------------
   Change Activity:
                   2017/4/14: 
-------------------------------------------------
"""
__author__ = 'JHao'

from blog.models import Category, Article


def sidebar(request):
    category_list = Category.objects.all()
    # 所有类型

    article_rank = Article.objects.all().order_by('-view')
    if len(article_rank) >= 6:
        article_rank = article_rank[0:6]
    return {
        'category_list': category_list,
        'article_rank': article_rank

    }


if __name__ == '__main__':
    pass
