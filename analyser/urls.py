from django.urls import path
from . import views


app_name = 'analyser'

urlpatterns = [
    path('savings_calculator/', views.savings_calculator_view,
         name='savings_calculator'),
    # path('<slug:slug>/', views.blog_post_detail_view, name='post-detail'),

]
