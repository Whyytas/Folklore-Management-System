from django.urls import path
from Rehearsals import views

urlpatterns = [
    path('', views.rehearsals_list, name='rehearsals'),
    path('add/', views.rehearsal_create, name='repeticija_create'),
    path('<int:pk>/edit/', views.rehearsal_edit, name='repeticija_edit'),
    path('<int:pk>/delete/', views.rehearsal_delete, name='repeticija_delete'),
    path('<int:pk>/', views.rehearsal_detail, name='repeticija_detail'),
]
