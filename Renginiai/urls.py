from django.urls import path
from .views import events_list

urlpatterns = [
    path('', events_list, name='renginiai'),
]
