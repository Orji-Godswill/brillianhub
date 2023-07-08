from django.urls import path
from . import views


app_name = 'analyser'

urlpatterns = [
    path('', views.analyser_view, name='analyser'),
    # path('<slug:slug>/', views.blog_post_detail_view, name='post-detail'),

]