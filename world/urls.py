from django.urls import path
from . import views, functions
from .views import PropDetailView

urlpatterns = [
    path('', views.home, name='world-home'),
    path('about/', views.about, name='world-about'),
    path('search/', views.search, name='world-search'),
    path('overpass/<int:pk>', views.overpass_test, name='overpass'),
    path('results/<int:pk>/', PropDetailView.as_view(), name='prop-detail'),
    path('addfavourite/<int:pk>/', views.addfave, name='add-fave'),
    path('removefavourite/<int:pk>/', views.removefave, name='remove-fave'),
]