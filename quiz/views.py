# quiz/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice
import random
from django.http import JsonResponse
import json
from course.models import Module


def random_question(request, pk=None):
    # Get a random question

    module = get_object_or_404(Module, pk=pk)

    question = random.choice(Question.objects.filter(module__id=module.id))
    next_question = question.get_next_question()

    context = {
        'question': question,
        'next_question': next_question
    }

    return render(request, 'quiz/quiz_list.html', context)


def check_answer(request):
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
        else:
            is_correct = False

        return JsonResponse({'selectChoice': select_choice, 'is_correct': is_correct})
    return JsonResponse({'error': 'Invalid request'})
