from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('addProduct/', views.add_product, name='add product'),
    path('test/', views.test_connection, name='test'),  # Changed from 'endpoint/' to 'test/' to match React code
]