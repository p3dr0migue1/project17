# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    posts = Post.published.all()
    context {'posts': posts}

    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)
    context = {'post': post}

    return render(request, 'blog/post/detail.html', context)
