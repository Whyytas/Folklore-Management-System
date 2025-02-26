from django.urls import path
from .views import *

urlpatterns = [
    path('', programos_page, name='programos'),
    path('prideti/', program_create, name='program_create'),
    path('<int:pk>/kuriniai/', programos_kuriniai_view, name='programos_kuriniai'),
    path('<int:pk>/edit/', program_edit, name='program_edit'),
    path('<int:pk>/delete/', istrinti_programa, name='program_delete'),

]
