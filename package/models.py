from __future__ import unicode_literals
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.urls import reverse
import random
from django.db.models import Q
import os
from django.db.models.signals import pre_save, post_save
from brillianzhub.utils import unique_slug_generator, unique_package_key_generator
from taggit.managers import TaggableManager
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.


class AssetQuerySet(models.query.QuerySet):
    def featured(self):
        return self.queryset().filter(featured=True)

    def published(self):
        return self.filter(status='published')

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__in=[query]) |
            Q(category__icontains=query) |
            Q(cost__icontains=query)
        )
        return self.filter(lookups).distinct()


class AssetManager(models.Manager):
    def get_queryset(self):
        return AssetQuerySet(self.model, using=self._db)

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
    return "package/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Package(models.Model):
    STATUS_CHOICES = (
        ('closed', 'Closed'),
        ('open', 'Open'),
    )

    LISTED_CHOICE = (
        ('L', 'Listed'),
        ('Del', 'Delisted')
    )

    CATEGORY_CHOICES = (
        ('apartment', 'APARTMENT'),
        ('duplex', 'Duplex'),
        ('hostel', 'Hostel'),
        ('land', 'Land'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='package_users', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    investor = models.DecimalField(max_digits=10, decimal_places=0)
    slug = models.SlugField(blank=True, unique=True)
    image = models.FileField(
        upload_to=upload_image_path, null=True, blank=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    description = RichTextUploadingField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=250)
    package_key = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    listed = models.CharField(
        max_length=3, choices=LISTED_CHOICE, default='Del')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='land')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='open')
    publish = models.DateTimeField(default=timezone.now)

    objects = AssetManager()
    tags = TaggableManager()
    search = AssetManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('package:package_detail', kwargs={'slug': self.slug})


def pre_save_create_package_key(sender, instance, *args, **kwargs):
    if not instance.package_key:
        instance.package_key = unique_package_key_generator(instance)


pre_save.connect(pre_save_create_package_key, sender=Package)


def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(post_pre_save_receiver, sender=Package)


class Property(models.Model):
    STATUS_CHOICES = (
        ('closed', 'Closed'),
        ('open', 'Open'),
    )

    LISTED_CHOICE = (
        ('L', 'Listed'),
        ('Del', 'Delisted')
    )

    CATEGORY_CHOICES = (
        ('apartment', 'APARTMENT'),
        ('duplex', 'Duplex'),
        ('hostel', 'Hostel'),
        ('land', 'Land'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='property_users', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, unique=True)
    image = models.FileField(
        upload_to=upload_image_path, null=True, blank=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    description = RichTextUploadingField()
    area = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=250)
    property_key = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    listed = models.CharField(
        max_length=3, choices=LISTED_CHOICE, default='Del')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='land')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='open')
    publish = models.DateTimeField(default=timezone.now)

    objects = AssetManager()
    tags = TaggableManager()
    search = AssetManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('package:package_detail', kwargs={'slug': self.slug})


def pre_save_create_package_key(sender, instance, *args, **kwargs):
    if not instance.package_key:
        instance.package_key = unique_package_key_generator(instance)


pre_save.connect(pre_save_create_package_key, sender=Package)


def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(post_pre_save_receiver, sender=Package)
