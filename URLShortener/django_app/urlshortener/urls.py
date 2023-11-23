from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.createShortURL, name='create'),
    path('<str:url>/', views.redirect, name='redirect')
]