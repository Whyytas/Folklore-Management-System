from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.kuriniai_list, name='kuriniai'),
    path('prideti/', views.kuriniai_add, name='kuriniai_add'),
    path("<int:kurinys_id>/edit/", kuriniai_edit, name="kuriniai_edit"),
    path("<int:kurinys_id>/delete/", delete_kurinys, name="kuriniai_delete"),
    path('refresh-trukme/', refresh_trukme, name='refresh_trukme'),
]
