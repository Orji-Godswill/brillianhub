from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('enrolled-courses/', views.StudentCourseListView.as_view(),
         name='enrolled_courses'),

    path('enroll_for_course/', views.StudentEnrollCourseView.as_view(),
         name='enroll'),

    path('percentage-completion/<int:course_id>/',
         views.percentage_completion, name='percentage_completion'),
    path('confirm-completion/<int:topic_id>/',
         views.confirm_completion, name='confirm_completion'),

]
