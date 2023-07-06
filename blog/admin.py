from django.contrib import admin
from .models import Blog


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display            = ('title', 'slug', 'user', 'publish', 'status')
    list_filter             = ('status', 'created', 'publish', 'user')
    search_fields           = ('title', 'body')
    raw_id_fileds           = ('user',)
    date_hierarchy          = 'publish'
    ordering                = ['status', 'publish']

admin.site.register(Blog, BlogAdmin)


# class CommentAdmin(admin.ModelAdmin):
#     list_display            = ('name', 'email', 'blog', 'created', 'active')
#     list_filter             = ('active', 'created', 'updated')
#     search_fields           = ('name', 'email', 'comment')

# admin.site.register(Comment, CommentAdmin)
