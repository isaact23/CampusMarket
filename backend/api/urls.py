from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('test/', views.test_connection, name='test'),  # Changed from 'endpoint/' to 'test/' to match React code
]