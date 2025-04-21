from django.urls import path
from .views import *
urlpatterns = [

    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', custom_logout, name='logout'),  # Use the custom logout view
    path('', main_page, name='main'),
    path("set-ansamblis/", set_selected_ensemble, name="set_selected_ansamblis"),

]
