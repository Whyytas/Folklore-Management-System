from django.urls import path
from .views import calendar_view, calendar_events

urlpatterns = [
    path('', calendar_view, name="kalendorius"),
    path('events/', calendar_events, name="kalendorius_events"),
]
