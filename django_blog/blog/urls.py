# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     urls.py  
   Description :  
   Author :       JHao
   date：          2017/4/13
-------------------------------------------------
   Change Activity:
                   2017/4/13: 
-------------------------------------------------
"""
__author__ = 'JHao'

from blog import views
from django.conf.urls import url

urlpatterns = [

    url(r'^index/$', views.Index, name='index'),
    url(r'^about/$', views.About, name='about'),
]
