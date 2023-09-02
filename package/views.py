from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Package
from order.models import Order
from order.forms import OrderForm
from django.contrib import messages
from django.contrib.auth import get_user_model


def packages_view(requests):
    packages = Package.objects.filter(status='published')
    context = {
        'packages': packages,
    }

    return render(requests, 'packages/packages.html', context)


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
