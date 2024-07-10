# weather/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.get_weather, name='get_weather'),
    path('', views.weather_list, name='weather_list'),
    path('weather/<int:pk>/', views.weather_detail, name='weather_detail'),
    path('weather/create/', views.weather_create, name='weather_create'),
    path('weather/update/<int:pk>/', views.weather_update, name='weather_update'),
    path('weather/delete/<int:pk>/', views.weather_delete, name='weather_delete'),
]
