from django.urls import path
from .views import  main

urlpatterns = [

    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', custom_logout, name='logout'),  # Use the custom logout view
    path('', main, name='main'),



]
