from django.urls import path
from . import views

app_name = 'quiz'


urlpatterns = [
    path('check_answer/', views.check_answer, name='check_answer'),
    path('question/<int:pk>/', views.QuestionDetailView.as_view(),
         name='question_content'),
    path('quiz/complete/', views.quiz_complete, name='quiz_complete'),

]
