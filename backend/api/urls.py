from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('test/', views.test_connection, name='test')  # Changed from 'endpoint/' to 'test/' to match React code
]