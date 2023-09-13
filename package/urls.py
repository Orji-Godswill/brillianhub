from django.urls import path
from . import views


app_name = 'package'

urlpatterns = [
    path('', views.packages_view, name='packages'),
    path('<slug:slug>/', views.package_detail_view, name='package_detail'),
    path('create/add-new-package/', views.package_create_view, name='package_create'),
]
