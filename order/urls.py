from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.investment_list_view, name='investment'),
    path('<slug:slug>/', views.invest_now_view, name='invest_now'),
    path('product/', views.add_earning_view, name='earn')
]
