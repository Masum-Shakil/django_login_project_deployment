from django.contrib import admin
from django.urls import path, include
from login_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
]