from django.urls import path
from .views import instrumentai_list, instrumentai_add, instrumentai_edit, instrumentai_delete

urlpatterns = [
    path("", instrumentai_list, name="instrumentai_list"),
    path("add/", instrumentai_add, name="instrumentai_add"),
    path("<int:pk>/edit/", instrumentai_edit, name="instrumentai_edit"),
    path("<int:pk>/delete/", instrumentai_delete, name="instrumentai_delete"),
]
