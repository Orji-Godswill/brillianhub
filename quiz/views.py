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

        if next_question:
            print(f"Next Question: {next_question}")
        else:
            print("No more questions")

        course = Course.objects.all()
        context['course'] = course
        module = question.module
        context['module'] = module

        return context


def quiz_complete(request):

    result = 0

    context = {

    }

    return render(request, 'quiz/quiz_complete.html', context)


def check_answer(request):
    pass_test = 0
    failed_test = 0

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
            pass_test += 1
            print(f"Pass = {pass_test}")
        else:
            is_correct = False
            failed_test += 1
            print(f"Failed = {failed_test}")

        return JsonResponse({'selectChoice': select_choice, 'is_correct': is_correct})
    return JsonResponse({'error': 'Invalid request'})


def calculate_time(request, pk):

    context = {

    }

    return render(request, '', context)
