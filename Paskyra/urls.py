from django.urls import path
from . import views

urlpatterns = [
    path('', views.paskyra_page, name='paskyra'),
]
