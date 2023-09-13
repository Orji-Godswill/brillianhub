from django.shortcuts import render, get_object_or_404
from .models import Dividend
from package.models import Package
# Create your views here.


def list_income_view(request, *args, **kwargs):
    slug = kwargs.get('slug')
    package = get_object_or_404(Package, slug=slug)
    income = Dividend.income.filter(package__title=package.title)

    ls = []
    total = 0
    for obj in income:
        ls.append(float(obj.amount))

    for num in ls:
        total += num

    for k in income:
        print(k.amount)

    context = {
        'income': income,
        'total': total,
    }

    return render(request, 'income/list_income.html', context)
