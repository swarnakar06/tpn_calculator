from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('calculate/', views.calculate_ratio, name='calculate_ratio'),
]
