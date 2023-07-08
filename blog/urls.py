from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.blog_posts_view, name='posts'),
    path('<slug:slug>/', views.blog_post_detail_view, name='post-detail'),
]