from django.urls import path
from . import views
from .views import event_pdf_view

urlpatterns = [
    path('', views.events_list, name='renginiai'),
    path('prideti/', views.events_add, name='renginiai_add'),
    path('<int:event_id>/edit/', views.events_edit, name='renginiai_edit'),
    path('<int:event_id>/delete/', views.event_delete, name='renginiai_delete'),
    path('public/', views.publicEvents, name='publicEvents'),
    path('<int:event_id>/pdf/', event_pdf_view, name='event_pdf'),
    path('<int:event_id>/nariai/', views.users_for_event, name='nariai_for_renginys'),

]
