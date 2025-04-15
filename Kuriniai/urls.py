from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.kuriniai_list, name='kuriniai'),
    path('prideti/', views.kuriniai_add, name='kuriniai_add'),
    path("<int:kurinys_id>/edit/", kuriniai_edit, name="kuriniai_edit"),
    path("<int:kurinys_id>/delete/", delete_kurinys, name="kuriniai_delete"),
    path("api/fetch_trukme/", fetch_trukme, name="fetch_trukme"),
    path("by-ansamblis-pozymis/", views.kuriniai_by_ansamblis_pozymis, name="kuriniai_by_ansamblis_pozymis"),
    path("<int:kurinys_id>/details/", views.kurinys_details, name="kurinys_details")
]
