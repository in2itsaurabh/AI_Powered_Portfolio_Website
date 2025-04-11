from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('upload/', views.upload_csv, name='upload_csv'),
    # path('process_forecast/', views.process_forecast, name='process_forecast'),
    path('contact/', views.contact, name='contact'),
    path('ask/', views.chatbot_response, name='chatbot_response'),
] 