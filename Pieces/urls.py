from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.pieces_list, name='pieces'),
    path('prideti/', views.piece_add, name='pieces_add'),
    path("<int:piece_id>/edit/", piece_edit, name="pieces_edit"),
    path("<int:piece_id>/delete/", piece_delete, name="pieces_delete"),
    path("api/fetch_duration/", fetch_duration, name="fetch_duration"),
    path("by-ansamblis-pozymis/", views.pieces_by_ensemble_feature, name="pieces_by_ensemble_feature"),
    path("<int:piece_id>/details/", views.piece_details, name="piece_details")
]
