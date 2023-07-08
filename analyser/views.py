from django.shortcuts import render, redirect
# from .models import Blog
from django.urls import reverse_lazy
from taggit.models import Tag
# Create your views here.


def analyser_view(request):
    # stock = Blog.objects.all().published()

    return render(request, 'analyser/calculator.html')
    