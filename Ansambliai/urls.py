from django.urls import path
from . import views

urlpatterns = [
    path('', views.ensembles_page, name='ensembles'),
]
