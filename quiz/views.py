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

        count = 0
        next_question = question.get_next_question()
        context['next_question'] = next_question

        course = Course.objects.all()
        context['course'] = course
        module = question.module
        context['module'] = module

        return context

    def update_progress_bar(request):
        current_value = int(request.POST.get('current_value', 0))
        print(current_value)


class QuestionsDetailView(DetailView):
    model = Question
    template_name = 'quiz/question_content.html'
    context_object_name = 'question'

    def get(self, request, *args, **kwargs):
        question = self.get_object()

        count = 0
        next_question = question.get_next_question()

        course = Course.objects.all()

        # Create a dictionary to serialize as JSON
        json_response = {
            'next_question': {
                'id': next_question.id,
                # 'content': next_question.content,
                # Add other fields as needed
            },
            'course': [{'id': c.id, 'title': c.title} for c in course],
            # Adjust fields accordingly
            'module': {'id': question.module.id, 'title': question.module.title},
        }

        return JsonResponse(json_response)


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


def quiz_complete(request):

    user_quiz_score = 0
    if request.user in quiz_score:
        user_quiz_score = quiz_score[request.user] * 10

    context = {
        'user_quiz_score': user_quiz_score,
    }

    return render(request, 'quiz/quiz_complete.html', context)


def calculate_time(request, pk):

    context = {

    }

    return render(request, '', context)
