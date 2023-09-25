from django.urls import path, re_path
from . import views

app_name = 'course'

urlpatterns = [
    path('stocks/', views.course_stocks_list_view, name='stocks'),
    path('real_estate/', views.course_real_list_view, name='real_estate'),
    path('finacial_management/',
         views.course_finance_list_view, name='financial_mgt'),

    path('', views.CourseListView.as_view(), name='course_list'),
    re_path(r'^detail/(?P<slug>[\w-]+)/$',
            views.CourseDetailView.as_view(), name='course_detail'),
    re_path(r'^category/(?P<category_slug>[\w-]+)/$',
            views.course_by_category, name='list_category')
]
