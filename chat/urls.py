from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='home'),
    path('update_model', views.update_model, name='update_model'),
    path('upload_pdf', views.upload_pdf, name='upload_pdf'),
    path('chat', views.chat, name='chat'),
]