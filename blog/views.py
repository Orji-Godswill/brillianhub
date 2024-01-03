from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Category
from django.urls import reverse_lazy
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# Create your views here.


def blog_posts_view(request, tag_slug=None):
    post = Blog.objects.all().published()
    category = Category.objects.all()

    tag = None
    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        post = Blog.objects.filter(tags__in=[tag])
    paginator = Paginator(post, 10)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    context = {
        'tag': tag,
        'post': post,
        'page': page,
        'category': category,
        'seo_title': 'Brillinazhub: Finance & Investment training hub'
    }
    return render(request, 'blog/posts.html', context)


def blog_post_detail_view(request, *args, **kwargs):
    slug = kwargs.get('slug')
    post = get_object_or_404(Blog, slug=slug)
    categories = Category.objects.all()

    post_tags_ids = post.tags.values_list('id', flat=True)
    print(post_tags_ids)
    related_posts = Blog.objects.all().published().filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    related_posts = related_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        'post': post,
        'categories': categories,
        'seo_title': post.title,
        'og_title': post.title,
        'related_posts': related_posts,
        'og_image': post.image.url,
        'og_description': post.description
    }

    return render(request, 'blog/details.html', context)
