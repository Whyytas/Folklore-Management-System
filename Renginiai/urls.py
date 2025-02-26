from django.urls import path
from .views import *

urlpatterns = [
    path('', events_list, name='ensembleEvents'),
    path('public/', publicEvents, name='publicEvents'),
]
