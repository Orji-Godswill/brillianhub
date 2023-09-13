from django.urls import path
from . import views

app_name = 'dividend'

urlpatterns = [
    path('<slug:slug>/', views.list_income_view, name='income_list')
]
