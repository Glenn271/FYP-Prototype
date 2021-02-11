from django.urls import path
from . import views
from .views import PropListView,PropDetailView
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='world-home'),
    path('about/', views.about, name='world-about'),
    path('search/', views.search, name='world-search'),
    path('results/', PropListView.as_view(), name='world-results'),
    # path('results/<int:pk>/', PropDetailView.as_view(), name='prop-detail'),
    url(r'^results/(?P<pk>\d+)/$', PropDetailView.as_view(), name='prop-detail'),
]