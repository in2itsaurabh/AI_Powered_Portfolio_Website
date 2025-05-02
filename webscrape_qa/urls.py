from django.urls import path
from . import views

urlpatterns = [
    path('', views.webscrape_combined, name='webscrape_combined'),
]
