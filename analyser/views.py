from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from taggit.models import Tag
import math
from . forms import SavingsCalculationForm, SavingsTargetForm, StockReturnForm
from django.http import JsonResponse
from datetime import datetime, timedelta

from . import utils


def one_year_ago_from_today():
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)
    return one_year_ago


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


def savings_target_calculator(request):

    if request.method == "POST":
        form = SavingsTargetForm(request.POST)

        if form.is_valid():
            target_amount = float(request.POST['target_amount'])
            initial_deposit = float(request.POST['initial_deposit'])
            duration = float(request.POST['duration'])
            interest_rate = float(request.POST['interest_rate'])
            rate_of_return = float(request.POST['rate_of_return'])

            parameter1 = ((interest_rate / 12) * 0.01)
            parameter2 = (
                ((1 + parameter1) ** (duration * 12)) - 1)

            result = (target_amount / (parameter2 / parameter1))

            result = round(result, 2)
            savings = round(initial_deposit + duration * result * 12, 2)
            profit = round(target_amount - savings, 2)

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
        form = SavingsTargetForm()

    context = {
        'form': form

    }

    return render(request, 'analyser/savings_target.html', context)


def return_on_stock_investment(request):
    context = {}
    invested_amount = 1000
    if request.method == 'POST':
        form = StockReturnForm(request.POST)
        if form.is_valid():
            symbol = request.POST['symbol'].upper()
            invested_amount = float(request.POST['invested_amount'])
            time_period = request.POST.get('time_period')

            if time_period == 'one_month':
                start_date = utils.one_month_from_today().strftime('%Y-%m-%d')
                period = 21
            elif time_period == 'one_year':
                start_date = utils.one_year_from_today().strftime('%Y-%m-%d')
                period = 252
            elif time_period == 'two_year':
                start_date = utils.two_years_from_today().strftime('%Y-%m-%d')
                period = 252 * 2
            elif time_period == 'five_year':
                start_date = utils.five_years_from_today().strftime('%Y-%m-%d')
                period = 252 * 5
            else:
                start_date = one_year_ago_from_today().strftime('%Y-%m-%d')
                period = 252

            end_date = utils.today

            stock_ticker, x_data, y_data, average_return = utils.analyse_stock_data(
                symbol, start_date, end_date)

            pct_return = average_return * period * 100
            pct_return = round(pct_return, 2)
            investment_return = pct_return * 0.01 * invested_amount
            investment_return = round(investment_return, 2)
            total_return = round((invested_amount + investment_return), 2)

            chart = utils.get_plot(x_data, y_data)
            context = {
                'success': True,
                'chart': chart,
                'stock_ticker': stock_ticker,
                'invested_amount': invested_amount,
                'pct_return': pct_return,
                'investment_return': investment_return,
                'total_return': total_return,
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = StockReturnForm()

    context = {
        'form': form,
        'invested_amount': invested_amount
    }

    return render(request, 'analyser/stock_return.html', context)


def return_on_real_estate_investment(request):

    context = {
    }
    return render(request, 'analyser/real_estate_roi.html', context)
