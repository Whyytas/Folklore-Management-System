from django.urls import path
from . import views

urlpatterns = [
    path('', views.ansambliai_list, name='ansambliai_list'),
    path('add/', views.ansamblis_add, name='ansamblis_add'),
    path('<int:pk>/edit/', views.ansamblis_edit, name='ansamblis_edit'),
    path('<int:pk>/delete/', views.ansamblis_delete, name='ansamblis_delete'),
]