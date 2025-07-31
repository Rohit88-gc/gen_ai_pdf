from django.urls import path
from . import views

app_name = 'smart_pdf_app'

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('chat/', views.chat, name='chat'),
]
