from django.urls import path
from . import views
from .views import filtered_kuriniai

urlpatterns = [
    path('', views.ansambliai_list, name='ansambliai_list'),
    path('add/', views.ansamblis_add, name='ansamblis_add'),
    path('<int:pk>/edit/', views.ansamblis_edit, name='ansamblis_edit'),
    path('<int:pk>/delete/', views.ansamblis_delete, name='ansamblis_delete'),
    path('<int:pk>/kuriniai/', views.get_kuriniai_by_ansamblis, name='get_kuriniai_by_ansamblis'),
    path("<int:ansamblis_id>/kuriniai/filter/", filtered_kuriniai, name="filtered_kuriniai"),


]