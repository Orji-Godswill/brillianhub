from django.urls import path
from . import views

app_name = 'referral'
urlpatterns = [
    path('', views.referral_list_view, name='referral_view'),
]
