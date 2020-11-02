from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='world-home'),
    path('about/', views.about, name='world-about'),
]