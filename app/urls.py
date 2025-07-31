from django.urls import path
from .views import home, download_forecast_pdf, forecast



urlpatterns = [
    path('', home, name='home'),
    # path('weekly/', weekly_forecast, name='weekly_forecast'),
    path('forecast/pdf/', download_forecast_pdf, name='download_forecast_pdf'),  
    path('forecast/', forecast, name='forecast'),
]