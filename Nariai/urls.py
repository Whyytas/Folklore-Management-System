from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.nariai_list, name='nariai'),
    path('add/', nariai_add, name='nariai_add'),
    path('<int:user_id>/', nariai_view, name='nariai_view'),
    path('<int:user_id>/edit/', nariai_edit, name='nariai_edit'),
    path('<int:user_id>/delete/', nariai_delete, name='nariai_delete'),
]
