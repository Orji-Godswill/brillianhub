from bs4 import BeautifulSoup
from typing import Any
from .models import Question
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
import random
from django.http import JsonResponse
import json
from course.models import Module, Topic, Course, Content
from django.core.serializers import serialize
from django.views.generic import DetailView, ListView


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'quiz/question_content.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(pk=None, **kwargs)
        question = self.object

        course = Course.objects.all()

        count = 0
        next_question = question.get_next_question()

        progress_bar = (question.order) * 10

        module = question.module

        context['next_question'] = next_question
        context['progress_bar'] = progress_bar
        context['course'] = course
        context['module'] = module

        return context


quiz_score = {}


def check_answer(request):

    user = request.user

    if request.method == 'POST':
        select_choice = request.POST.get('selectChoice', None)
        question_id = request.POST.get('question_id')

        choices = Choice.objects.filter(question__id=question_id)

        is_correct = None
        for choice in choices:
            if choice.is_correct == True:
                is_correct = choice

        if str(select_choice) == str(is_correct):
            is_correct = True

            if user not in quiz_score:
                quiz_score[user] = 0
            quiz_score[user] += 1

        else:
            is_correct = False

        return JsonResponse({'selectChoice': select_choice, 'is_correct': is_correct})
    return JsonResponse({'error': 'Invalid request'})


def show_score(request):
    pass


def quiz_complete(request):

    user_quiz_score = 0
    if request.user in quiz_score:
        user_quiz_score = quiz_score[request.user] * 10

    last_question_id = int(request.POST.get('last_question_id'))
    last_question_order = int(request.POST['last_question_order'])
    first_question_id = last_question_id - (last_question_order - 1)

    last_question_course_id = request.POST['last_question_course_id']
    last_question_course_slug = request.POST['last_question_course_slug']

    context = {
        'user_quiz_score': user_quiz_score,
        'first_question_id': first_question_id,
        'last_question_course_id': last_question_course_id,
        'last_question_course_slug': last_question_course_slug
    }

    return render(request, 'quiz/quiz_complete.html', context)


def calculate_time(request, pk):

    context = {

    }

    return render(request, '', context)
