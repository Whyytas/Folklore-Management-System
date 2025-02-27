from django.urls import path
from . import views

urlpatterns = [
    path('', views.renginiai_list, name='renginiai'),
    path('prideti/', views.renginiai_add, name='renginiai_add'),
    path('<int:renginys_id>/edit/', views.renginiai_edit, name='renginiai_edit'),
    path('<int:renginys_id>/delete/', views.delete_renginys, name='renginiai_delete'),
    path('public/', views.publicEvents, name='publicEvents'),
]
