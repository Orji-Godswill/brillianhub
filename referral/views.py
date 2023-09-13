from django.shortcuts import render
from .models import Referrer, Payout, Earn
from order.models import Order
from .forms import PayoutForm
from django.contrib import messages
# Create your views here.


def referral_list_view(request, *args, **kwargs):

    referral = Referrer.objects.filter(referrer=request.user)

    context = {
        'referral': referral,
    }
    return render(request, 'referral/referral_list.html', context)


def my_referrals_view(request, *args, **kwargs):
    earnings = Order.objects.filter(referrer=request.user, status='paid')

    referrer = request.user

    pay = Payout.objects.filter(name=referrer)

    qs2 = list(pay.values('amount'))
    withdrawn = sum(item['amount'] for item in qs2)

    y = list(earnings.values('amount'))
    x = sum(item['amount'] for item in y)

    bd = float(x) * 0.2

    balance = float(bd) - float(withdrawn)

    earn = Earn.objects.filter(referrer=referrer).update(
        earn=bd, withdrawn=withdrawn, balance=balance)

    form = PayoutForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            payout_request = form.save(commit=False)
            amount = form.cleaned_data.get('amount')
            email = form.cleaned_data.get('email')

            if float(amount) > float(balance):
                payout_request = form.save(commit=False)
                messages.error(request, 'Sorry you have insufficient balance!')
            else:
                payout_request.amount = amount
                payout_request.name = referrer
                payout_request.save()
                return render(request, 'referral/payout.html', {'payout_request': payout_request})
        else:
            form = PayoutForm()
    context = {
        'earnings': earnings,
        'balance': balance,
        'bd': bd,
        'withdrawn': withdrawn,
        'form': form,
    }
    return render(request, 'referral/ref_earning.html', context)


def payout_request_view(request):

    context = {

    }
    return render(request, 'referrals/payout.html', context)
