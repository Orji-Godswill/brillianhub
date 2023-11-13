from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('enrolled-courses/', views.enrolled_courses, name='enrolled_courses'),
    path('percentage-completion/<int:course_id>/',
         views.percentage_completion, name='percentage_completion'),
    path('confirm-completion/<int:topic_id>/',
         views.confirm_completion, name='confirm_completion'),
    # Add more URL patterns as needed
]
