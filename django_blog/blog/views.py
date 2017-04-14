# -*- coding: utf-8 -*-
# Create your views here.

from django.shortcuts import render


def Index(requests):
    return render(requests, 'blog/index.html', {"html_title": u"博客首页",
                                                "source_id": "index"})


def About(request):
    return render(request, 'Arctile_detail.html')
