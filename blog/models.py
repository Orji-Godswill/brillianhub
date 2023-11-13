from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.urls import reverse
import random
from django.db.models import Q
import os
from django.db.models.signals import pre_save, post_save
from brillianzhub.utils import unique_slug_generator
from taggit.managers import TaggableManager
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class BlogQuerySet(models.query.QuerySet):

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def published(self):
        return self.filter(status='published')

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__name__in=[query])
        )
        return self.filter(lookups).distinct()


class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910233549)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "blog/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='accounts_users', on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, related_name='post_category', on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = BlogManager()
    tags = TaggableManager()
    search = BlogManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'slug': self.slug})


def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(post_pre_save_receiver, sender=Blog)


# class Comment(models.Model):
#     graduate    = models.ForeignKey(Graduate, related_name='response_graduate', on_delete=models.CASCADE)
#     name        = models.CharField(max_length=250)
#     email       = models.EmailField(max_length=200, blank=True)
#     comment     = models.TextField()
#     created     = models.DateTimeField(auto_now_add=True)
#     updated     = models.DateTimeField(auto_now=True)
#     active      = models.BooleanField(default=True)

#     class Meta:
#         # sort comments in chronological order by default
#         ordering = ('created',)

#     def __str__(self):
#         return 'Comment by {}'.format(self.name)
