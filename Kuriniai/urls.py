from django.urls import path
from . import views

urlpatterns = [
    path('', views.kuriniai_page, name='kuriniai'),
]
