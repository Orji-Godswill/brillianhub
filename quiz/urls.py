from django.urls import path
from . import views

app_name = 'quiz'


urlpatterns = [
    path('quiz/<int:pk>/', views.random_question, name='test'),
    path('check_answer/', views.check_answer, name='check_answer'),
]
