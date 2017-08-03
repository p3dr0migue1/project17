# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published_date')
    author = models.ForeignKey(User, related_name='blog_posts')
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.published_date.year,
                              self.published_date.strftime('%m'),
                              self.published_date.strftime('%d'),
                              self.slug]
        )
