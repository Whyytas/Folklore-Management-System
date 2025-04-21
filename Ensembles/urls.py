from django.urls import path
from . import views
from .views import filtered_pieces

urlpatterns = [
    path('', views.ensembles_list, name='ansambliai_list'),
    path('add/', views.ensemble_add, name='ansamblis_add'),
    path('<int:pk>/edit/', views.ensemble_edit, name='ansamblis_edit'),
    path('<int:pk>/delete/', views.ensemble_delete, name='ansamblis_delete'),
    path('<int:pk>/kuriniai/', views.get_pieces_by_ensemble, name='get_kuriniai_by_ansamblis'),
    path("<int:ansamblis_id>/kuriniai/filter/", filtered_pieces, name="filtered_kuriniai"),


]