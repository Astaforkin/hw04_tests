from django.core.paginator import Paginator

LAST_POSTS = 10


def get_paginator(value, request):
    paginator = Paginator(value, LAST_POSTS)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
