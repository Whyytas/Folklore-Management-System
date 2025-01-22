from django.urls import path
from . import views

urlpatterns = [
    path('', views.programos_page, name='programos'),
]
