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

from blog.models import Category


def sidebar(request):
    category_list = Category.objects.all()
    return {
        'category_list': category_list
    }


if __name__ == '__main__':
    pass
