from django.urls import path, re_path, reverse_lazy, include
from . import views
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView,
)

from . import views


app_name = 'accounts'
urlpatterns = [
        path('', views.AccountHomeView.as_view(), name='account-home'),
        re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', views.AccountEmailActivationView.as_view(), name='email-activate'),
        re_path(r'^email/resend-activation/$', views.AccountEmailActivationView.as_view(), name='resend-activation'),
        path('login/', views.LoginView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_URL), name='logout'),
        path('register/', views.register_page, name='register'),
        path('edit/', views.edit, name='edit_profile'),
]
