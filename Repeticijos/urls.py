from django.urls import path
from Repeticijos import views

urlpatterns = [
    path('', views.repeticijos_list, name='repeticijos'),
    path('add/', views.repeticija_create, name='repeticija_create'),
    path('<int:pk>/edit/', views.repeticija_edit, name='repeticija_edit'),
    path('<int:pk>/delete/', views.repeticija_delete, name='repeticija_delete'),
    path('<int:pk>/', views.repeticija_detail, name='repeticija_detail'),
]
