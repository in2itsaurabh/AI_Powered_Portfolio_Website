from django.urls import path
from . import views

urlpatterns = [
    path('', views.rag_interface, name='rag_interface'),  # RAG interface page
    path('upload_pdf/', views.upload_pdf, name='rag_process_pdf'),  # Handle PDF uploads
    path('ask_question/', views.ask_question, name='rag_ask_question'),  # Handle questions
]
