from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Count
from .models import Course, Module, Topic, Content
from django.views.generic.base import TemplateResponseMixin, View


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_details.html"
    context_object_name = 'course'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.module_set.all()

        return context


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'courses/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.object
        context['next_topic'] = topic.get_next_topic()
        context['previous_topic'] = topic.get_previous_topic()

        return context


class FeaturedCourseView(ListView):
    template_name = "index.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Course.objects.featured()
