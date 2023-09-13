from django.urls import path
from .views import AssetPortfolio

app_name = 'portfolio'

urlpatterns = [
    path('', AssetPortfolio.land_property, name='land_property')
]
