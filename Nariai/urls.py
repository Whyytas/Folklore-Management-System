from django.urls import path
from . import views

urlpatterns = [
    path('', views.nariai_page, name='nariai'),
]
