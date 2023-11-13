from django.urls import path, re_path
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
]
