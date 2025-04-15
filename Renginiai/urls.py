from django.urls import path
from . import views
from .views import renginys_pdf_view

urlpatterns = [
    path('', views.renginiai_list, name='renginiai'),
    path('prideti/', views.renginiai_add, name='renginiai_add'),
    path('<int:renginys_id>/edit/', views.renginiai_edit, name='renginiai_edit'),
    path('<int:renginys_id>/delete/', views.delete_renginys, name='renginiai_delete'),
    path('public/', views.publicEvents, name='publicEvents'),
    path('<int:renginys_id>/pdf/', renginys_pdf_view, name='renginys_pdf'),
    path('<int:renginys_id>/nariai/', views.nariai_for_renginys, name='nariai_for_renginys'),

]
