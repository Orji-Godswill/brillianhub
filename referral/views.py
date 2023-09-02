from django.shortcuts import render
from .models import Referrer
# Create your views here.


def referral_list_view(requests, *args, **kwargs):

    referral = Referrer.objects.filter(referrer=requests.user)

    context = {
        'referral': referral,
    }
    return render(requests, 'referral/referral_list.html', context)
