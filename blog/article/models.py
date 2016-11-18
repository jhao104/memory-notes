# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     models.py  
   Description :  
   Author :       JHao
   date：          2016/11/18
-------------------------------------------------
   Change Activity:
                   2016/11/18: 
-------------------------------------------------
"""

# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.

class Article(models.Model):

    title = models.CharField(max_length=200)  # 博客标题
    category = models.CharField(max_length=50, blank=True)  # 博客标签
    date_time = models.DateField(auto_now_add=True)  # 博客日期
    content = models.TextField(blank=True, null=True)  # 博客正文
    author = models.CharField(max_length=20)  # 作者
    view = models.BigIntegerField(default=0)  # pv
    comment = models.BigIntegerField(default=0)  # 评论
    like = models.BigIntegerField(default=0)  # 喜欢 or 点赞
    classify = models.CharField(max_length=100)  # 分类

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        path = reverse('article:detail', kwargs={'id': self.id})
        return "http://127.0.0.1:8000%s" % path  # 给多说使用

    class Meta:  # 按时间降序
        ordering = ['-date_time']
