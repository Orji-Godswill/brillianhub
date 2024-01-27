from django.urls import path
from . import views


app_name = 'analyser'

urlpatterns = [
    path('savings_calculator/', views.savings_calculator_view,
         name='savings_calculator'),
    path('real_estate_roi/', views.return_on_real_estate_investment,
         name='real_estate_roi'),
    path('return_on_stock_investment/',
         views.return_on_stock_investment, name='stock_return'),
    path('savings_target_calculator/', views.savings_target_calculator,
         name="savings_target_calculator"),
]
