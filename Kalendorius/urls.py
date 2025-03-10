from django.urls import path
from .views import kalendorius_view, kalendorius_events

urlpatterns = [
    path('', kalendorius_view, name="kalendorius"),
    path('events/', kalendorius_events, name="kalendorius_events"),
]
