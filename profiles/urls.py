from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_biodata, name='view_biodata'),
    path('register/', views.register, name='register'),
    path('create/', views.create_biodata, name='create_biodata'),
    path('download/', views.download_pdf, name='download_pdf'),
]
