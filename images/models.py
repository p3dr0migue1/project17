from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)

    # database index is improved query performance
    # consider seting db_index=True for fields that
    # you frequently query using `filter`, `exclude` and
    # `order_by`
    #
    # foreign key fields or fields with unique=True
    # implies the creation of an index
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True
    )
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)