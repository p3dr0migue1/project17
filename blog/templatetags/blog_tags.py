import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post


register = template.Library()


# Processes the data and returns a string
@register.simple_tag
def total_posts():
    return Post.published.count()


# Processes the data and returns a rendered template
# with the context variable specified
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-published_date')[:count]
    return {'latest_posts': latest_posts}


# Processes the data and sets a variable in the context
# Assignment Tags are like Simple Tags but they store the result in a variable
@register.assignment_tag
def get_most_commented_posts(count=2):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
