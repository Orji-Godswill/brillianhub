from django.contrib import admin
from .models import Course, Module, Topic, Content


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  # Number of empty forms to display


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1  # Number of empty forms to display


class ContentInline(admin.TabularInline):
    model = Content
    extra = 1  # Number of empty forms to display


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline, TopicInline, ContentInline]


# @admin.register(Module)
# class ModuleAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Topic)
# class TopicAdmin(admin.ModelAdmin):
#     pass


# @admin.register(Content)
# class ContentAdmin(admin.ModelAdmin):
#     pass
