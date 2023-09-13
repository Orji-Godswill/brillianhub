from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.urls import reverse_lazy
from taggit.models import Tag
# Create your views here.


def blog_posts_view(request, tag_slug=None):
    post = Blog.objects.all().published()

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
    return render(request, 'blog/posts.html', {'tag': tag, 'post': post})
    

def blog_post_detail_view(request, *args, **kwargs):
    slug = kwargs.get('slug')
    post = get_object_or_404(Blog, slug=slug)

    context = {
        'post': post,
    }

    return render(request, 'blog/details.html', context)

