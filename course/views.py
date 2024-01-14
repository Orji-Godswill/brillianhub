from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Count
from .models import Course, Module, Topic, Content
from django.views.generic.base import TemplateResponseMixin, View
from quiz.models import Question
from quiz.views import quiz_score
from bs4 import BeautifulSoup
from students.forms import CourseEnrollForm
from students.models import Student


def count_words(text):
    soup = BeautifulSoup(text, 'html.parser')
    plain_text = soup.get_text()

    words = plain_text.split()
    num_words = len(words)

    return num_words


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_details.html"
    context_object_name = 'course'

    # def dispatch(self, request, *args, **kwargs):
    #     module = self.get_object()

    #     student_courses = Course.objects.all().filter(
    #         students__in=[self.request.user])

    #     if module.course not in student_courses.all():
    #         print("enrolled")

    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = self.object.module_set.all()

        related_courses = Course.objects.all()

        context['related_courses'] = related_courses

        course_title = self.object
        total_count = course_title.get_topic_count_for_course()

        context['form'] = CourseEnrollForm(initial={'course': self.object})

        context['total_count'] = total_count

        return context


class TopicDetailView(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = 'courses/topic_content.html'
    context_object_name = 'topic'

    def dispatch(self, request, *args, **kwargs):
        topic = self.get_object()

        student_courses = Course.objects.all().filter(
            students__in=[self.request.user])

        if topic.module.course not in student_courses.all():
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topic = self.object
        module = topic.module
        content = get_object_or_404(Content, topic__id=topic.id)

        topic_duration = round(count_words(content.text_content) / 200)

        quiz_score = context.get('quiz_score', [])
        if quiz_score:
            quiz_score.clear()

        context['next_topic'] = topic.get_next_topic()
        context['previous_topic'] = topic.get_previous_topic()

        related_courses = Course.objects.all()
        context['next_module'] = module.get_next_module()

        question = Question.objects.filter(module__id=module.id).first()
        context['question'] = question
        context['module'] = module
        context['topic_duration'] = topic_duration
        context['related_courses'] = related_courses

        return context

# class TopicDetailView(DetailView):
#     model = Topic
#     template_name = 'courses/topic_content.html'
#     context_object_name = 'topic'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         topic = self.object
#         module = topic.module
#         content = get_object_or_404(Content, topic__id=topic.id)
#         topic_duration = round(count_words(content.text_content)/200)

#         if len(quiz_score) > 0:
#             quiz_score.clear()

#         context['next_topic'] = topic.get_next_topic()
#         context['previous_topic'] = topic.get_previous_topic()

#         related_courses = Course.objects.all()
#         context['next_module'] = module.get_next_module()

#         question = Question.objects.filter(module__id=module.id).first()

#         context['question'] = question
#         context['module'] = module

#         context['topic_duration'] = topic_duration

#         context['related_courses'] = related_courses

#         return context


class FeaturedCourseView(ListView):
    template_name = "index.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Course.objects.featured()
