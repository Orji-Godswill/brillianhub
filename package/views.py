from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Package
from order.models import Order
from order.forms import OrderForm
from dividend.forms import DividendForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CreatePackageForm
from dividend.models import Dividend


def packages_view(request):
    packages = Package.objects.filter(status='published')
    context = {
        'packages': packages,
    }

    return render(request, 'packages/packages.html', context)


User = get_user_model()


def package_detail_view(request, *args, **kwargs):
    slug = kwargs.get('slug')
    package = get_object_or_404(Package, slug=slug)
    order_form = OrderForm(data=request.POST)

    if request.method == 'POST':
        if order_form.is_valid():
            package_order = order_form.save(commit=False)
            package_order.user = request.user
            package_order.package = package
            package_order.save()
            messages.success(
                request, "Order received with thanks. We would get across to you on the patment procedure after confirmation")
            return HttpResponseRedirect(package.get_absolute_url())
    else:
        package_order = OrderForm(initial={'user': request.user.id})

    context = {
        'package': package,
        'order_form': order_form,
    }

    return render(request, 'packages/package_detail.html', context)


def package_create_view(request):
    package_form = CreatePackageForm(request.POST)

    if request.method == 'POST':
        if package_form.is_valid():
            dividend = Dividend.objects.create(package=new_package, amount=0)
            print(dividend)
            new_package = package_form.save(commit=False)
            new_package.save()
            return render(request,
                          'packages/package_create_done.html',
                          {'new_package': new_package})
        else:
            package_form = CreatePackageForm(initial={'user': request.user.id})
    return render(request, 'packages/package_create.html', {'package_form': package_form})
