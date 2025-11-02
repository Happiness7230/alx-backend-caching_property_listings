from django.urls import path
from . import views

urlpatterns = [
    path('metrics/', views.redis_metrics, name='redis_metrics'),
    path('properties/', views.property_list, name='property_list'),
]
