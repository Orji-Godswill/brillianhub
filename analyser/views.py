from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from taggit.models import Tag
import math
from . forms import SavingsCalculationForm
from django.http import JsonResponse


def savings_calculator_view(request):

    if request.method == "POST":
        form = SavingsCalculationForm(request.POST)
        if form.is_valid():
            initial_amount = float(request.POST['initial_deposit'])
            installmental_payment = float(
                request.POST['installmental_payment'])
            duration = float(request.POST['duration'])
            interest_return_rate = float(request.POST['rate_of_return'])
            frequency_payment = float(
                request.POST['frequency_installment_payment'])
            interest_rate = float(request.POST['interest_rate'])

            result1 = initial_amount * \
                (1 + (0.01 * interest_rate / interest_return_rate)
                 ) ** (interest_return_rate * duration)
            x = ((1 + (0.01 * interest_rate / frequency_payment))
                 ** (frequency_payment * duration)) - 1
            result2 = (installmental_payment * x) / \
                (0.01 * interest_rate / frequency_payment)

            result = round(result1 + result2, 2)
            savings = round(initial_amount + duration *
                            installmental_payment * frequency_payment, 2)
            profit = round(result - savings, 2)

            context = {
                'success': True,
                'result': result,
                'savings': savings,
                'profit': profit
            }

            return JsonResponse(context)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = SavingsCalculationForm()

    context = {
        'form': form,
    }
    return render(request, 'analyser/compound_savings.html', context)
