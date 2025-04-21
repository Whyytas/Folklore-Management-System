from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.users_list, name='nariai'),
    path('add/', user_add, name='nariai_add'),
    path('<int:user_id>/', users_view, name='nariai_view'),
    path('<int:user_id>/edit/', user_edit, name='nariai_edit'),
    path('<int:user_id>/delete/', user_delete, name='nariai_delete'),
    path('check-username/', check_username, name='check_username'),
    path('profilis/', views.account_edit, name='profilis_edit'),

]
