from django import views
from django.urls import path
from django.contrib import admin
from .import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('prediction/', views.predPage, name='prediction')
]
