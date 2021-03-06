# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from haystack.query import SearchQuerySet

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 3
    template_name = 'blog/post/post_list.html'

    def get_queryset(self):
        return Post.published.all()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['section'] = 'blog'
        return context


@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             published_date__year=year,
                             published_date__month=month,
                             published_date__day=day)

    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }

    # posts by similarity
    # post_tags_ids = post.tags.values_lists('id',flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published_date')[:4]

    return render(request, 'blog/post/post_detail.html', context)


@login_required
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # form submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recomends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n comments: {}'.format(post.title, post_url, cd['comments'])
            send_mail(subject, message, 'pedro.miguel@live.co.uk', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {'post': post, 'form': form, 'sent': sent}

    return render(request, 'blog/post/post_share.html', context)


def post_search(request):
    form = SearchForm()

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()

            # count total results
            total_results = results.count()
        return render(request,
                      'blog/post/main.html',
                      {'form': form,
                       'cd': cd,
                       'results': results,
                       'total_results': total_results})
    return render(request, 'blog/post/main.html', {'form': form})
