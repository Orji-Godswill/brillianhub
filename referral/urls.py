from django.urls import path
from . import views

app_name = 'referral'
urlpatterns = [
    path('', views.referral_list_view, name='referral_view'),
    path('my_referrals/', views.my_referrals_view, name='my_referrals'),
    path('payment_request_recieved/', views.payout_request_view, name='payout'),
]
