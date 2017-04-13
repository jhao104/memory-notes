from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def Index(requests):
    return render(requests, 'blog/index.html')


def About(request):
    return render(request, 'Arctile_detail.html')
