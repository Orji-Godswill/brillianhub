from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Land
from package.models import Package, Property
from dividend.models import Dividend
from order.models import Order

# I can have multiple classes and use inheritance to share methods. E.g. Investors class, workers class, hybrid class etc


class User:
    User = get_user_model()

    def __init__(self, email):
        self.user = email


class AssetPortfolio():

    def land_property(request):
        land = Land.objects.filter(user=request.user)
        order = Order.objects.filter(user=request.user)
        property = Property.objects.filter(user=request.user)

        earn1 = Dividend.income.all()

        ls = []
        ls2 = []

        for i in earn1:
            ls.append(i.package.title)

        for n in order:
            ls2.append(n.package.title)

        my_dict = {}

        for earn in earn1:
            if not earn.package.title in my_dict:
                my_dict[earn.package.title] = float(earn.amount)
            else:
                my_dict[earn.package.title] += float(earn.amount)

        ls_earn1 = []
        total = 0

        for earn in earn1:
            ls_earn1.append(float(earn.amount))

        for item in ls_earn1:
            total += item

        context = {
            'land': land,
            'order': order,
            'property': property,
            'my_dict': my_dict,
        }

        return render(request, 'portfolio/portfolio.html', context)

    def savings(self):
        pass

    def totalin(self):
        pass

    def totalout(self):
        pass


u1 = AssetPortfolio()
