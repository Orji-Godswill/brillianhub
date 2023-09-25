from django.db import models
from django.db.models import Q
from django.conf import settings
from django.db.models.query import QuerySet
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import random
import os
from taggit.managers import TaggableManager
from brillianzhub.utils import unique_slug_generator
from .fields import OrderField


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_video_path(instance, filename):
    new_filename = random.randint(1, 3910233549)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "courses/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910233549)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "images/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_file_path(instance, filename):
    new_filename = random.randint(1, 3910233549)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "files/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return str(self.title)


def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(category_pre_save_receiver, sender=Category)


class CourseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(
            overview__icontains=query) | Q(tags__name__in=[query])
        return self.filter(lookups).distinct()


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)

        if qs.count() == 1:
            return qs.first()
        return None

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def search(self):
        return self.get_queryset().active().search()


class Course(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    overview = models.TextField()
    video = models.FileField(
        upload_to=upload_video_path, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='course_joined', blank=True)

    objects = CourseManager()

    tags = TaggableManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.title)


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Course)


class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name='course_modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Objective(models.Model):
    course = models.ForeignKey(
        Course, related_name='course_objective', on_delete=models.CASCADE)
    objectives = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.objectives)


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name='module_content', on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['module'])
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in': (
        'text', 'video', 'image', 'file')}, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to=upload_file_path)


class Image(ItemBase):
    image = models.FileField(upload_to=upload_image_path)


class Video(ItemBase):
    video = models.FileField(upload_to=upload_video_path)
