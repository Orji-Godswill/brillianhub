from django.shortcuts import render, get_object_or_404
from package.models import Package
from .models import Order
# Create your views here.


def investment_list_view(requests):
    investment = Order.objects.filter(user=requests.user)

    context = {
        'investment': investment,
    }

    return render(requests, 'investment/invest_list.html', context)


def invest_now_view(requests, *args, **kwargs):
    slug = kwargs.get('slug')
    investment_package = get_object_or_404(Package, slug=slug)

    context = {
        'investment_package': investment_package
    }

    return render(requests, 'investment/invest_now.html', context)


def add_earning_view(requests):
    order = Order.objects.filter(package='created')

    context = {
        'order': order
    }
    return render(requests, 'investment/earn.html', context)
