from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Count
from .models import Category, Course, Module, Content
from django.views.generic.base import TemplateResponseMixin, View


def course_stocks_list_view(request, *args, **kwargs):

    stock = Course.objects.filter(
        category__title__contains='stocks').distinct()

    context = {
        'stock': stock,

    }
    return render(request, 'courses/list.html', context)


def course_real_list_view(request, *args, **kwargs):

    real = Course.objects.filter(
        category__title__contains='real estate').distinct()

    context = {
        'real': real,
    }
    return render(request, 'courses/list.html', context)


def course_finance_list_view(request, *args, **kwargs):

    finance_mgt = Course.objects.filter(
        category__title__contains='financial management').distinct()

    context = {
        'finance_mgt': finance_mgt
    }
    return render(request, 'courses/list.html', context)


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/list.html'

    def get(self, request, category=None):
        categories = Category.objects.annotate(total_courses=Count('courses'))
        courses = Course.objects.annotate(
            total_modules=Count('course_modules'))

        if category:
            category = get_object_or_404(Category, slug=category)
            courses = courses.filter(category=category)
        return self.render_to_response({'categories': categories,
                                        'category': category,
                                        'courses': courses})


class CourseDetailView(DetailView):
    queryset = Course.objects.all()
    # model = Course
    template_name = "courses/course-details.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        return context


def course_by_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    courses = Course.objects.filter(category__slug=category_slug)
    context = {
        'category': category,
        'courses': courses
    }
    return render(request, 'courses/category_list.html', context)


class FeaturedCourseView(ListView):
    template_name = "index.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Course.objects.featured()
