from django.urls import path
from . import views

urlpatterns = [
    path('', views.instrumentai_page, name='instrumentai'),
]
