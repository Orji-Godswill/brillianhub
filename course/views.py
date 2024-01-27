from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Count
from .models import Course, Module, Topic, CompletedTopic, Content
from django.views.generic.base import TemplateResponseMixin, View
from quiz.models import Question
from quiz.views import quiz_score
from bs4 import BeautifulSoup
from students.forms import CourseEnrollForm
from students.models import Student
from django.http import JsonResponse


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['modules'] = self.object.module_set.all()

        related_courses = Course.objects.all()
        context['related_courses'] = related_courses

        completed_topics = CompletedTopic.objects.filter(
            user=self.request.user, topic__course=course, completed=True
        )

        my_courses = Course.objects.all().filter(
            students__in=[self.request.user])

        context['my_courses'] = my_courses

        completed_topic_ids = set(
            completed_topic.topic.id for completed_topic in completed_topics)

        topic_completion_dict = {
            topic.id: topic.id in completed_topic_ids for module in context['modules'] for topic in module.topic_set.all()}

        completed_topics_count = completed_topics.count()
        total_topics_course = Topic.objects.filter(course__id=course.id)

        try:
            percentage_completion = round((
                (completed_topics_count / total_topics_course.count()) * 100), 2)
        except:
            percentage_completion = 0.00

        context['completed_topics_count'] = completed_topics_count
        context['percentage_completion'] = percentage_completion
        context['topic_completion_dict'] = topic_completion_dict

        course_title = self.object
        total_count = course_title.get_topic_count_for_course()

        context['form'] = CourseEnrollForm(initial={'course': self.object})
        context['total_count'] = total_count

        return context


class CompletionMixin(LoginRequiredMixin, View):
    def update_completion_status(self, topic):
        completed_topic, created = CompletedTopic.objects.get_or_create(
            user=self.request.user,
            topic=topic
        )

        if not created and not completed_topic.completed:
            completed_topic.completed = True
            completed_topic.save()


class TopicDetailView(CompletionMixin, DetailView):
    model = Topic
    template_name = 'courses/topic_content.html'
    context_object_name = 'topic'

    def dispatch(self, request, *args, **kwargs):
        topic = self.get_object()

        student_courses = Course.objects.all().filter(
            students__in=[self.request.user])

        if topic.module.course not in student_courses.all():
            return redirect('home')

        self.update_completion_status(topic)

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

        try:
            context['next_topic'] = topic.get_next_topic()
        except:
            context['next_topic'] = None

        context['previous_topic'] = topic.get_previous_topic()

        related_courses = Course.objects.all()
        context['next_module'] = module.get_next_module()

        try:
            question = Question.objects.get(
                module=module, course=module.course, order=1)
        except Question.DoesNotExist:
            question = None
        except Question.MultipleObjectsReturned:
            question = None

        print(question)
        context['question'] = question
        context['module'] = module
        context['topic_duration'] = topic_duration
        context['related_courses'] = related_courses

        return context


class CompletedTopicsView(LoginRequiredMixin, View):
    template_name = 'courses/completed_topics.html'

    def get(self, request, course_id):
        user = self.request.user
        course = get_object_or_404(Course, id=course_id)

        completed_topics = CompletedTopic.objects.filter(
            user=user,
            topic__course=course,
            completed=True
        )

        completed_topics_count = completed_topics.count()

        total_topics_course = Topic.objects.filter(course__id=course.id)

        return render(request, self.template_name, {
            'course': course,
            'completed_topics': completed_topics,
            'completed_topics_count': completed_topics_count,
        })


class FeaturedCourseView(ListView):
    template_name = "index.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Course.objects.featured()
