from django.urls import path
from .views import (
    PadaliniaiListView,
    PadalinysCreateView,
    PadalinysUpdateView,
    PadalinysDeleteView,
)

urlpatterns = [
    path("", PadaliniaiListView.as_view(), name="padaliniai_list"),
    path("add/", PadalinysCreateView.as_view(), name="padaliniai_add"),
    path("<int:pk>/edit/", PadalinysUpdateView.as_view(), name="padaliniai_edit"),
    path("<int:pk>/delete/", PadalinysDeleteView.as_view(), name="padaliniai_delete"),
]
