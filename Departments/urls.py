from django.urls import path
from .views import *

urlpatterns = [
    path("", DepartmentsListView.as_view(), name="padaliniai_list"),
    path("add/", DepartmentCreateView.as_view(), name="padaliniai_add"),
    path("<int:pk>/edit/", department_edit, name="padaliniai_edit"),
    path("<int:pk>/delete/", DepartmentDeleteView.as_view(), name="padaliniai_delete"),
]
