from django.urls import path
from .views import *

urlpatterns = [
    path('', programs_list, name='programos'),
    path('prideti/', program_create, name='program_create'),
    path('<int:pk>/kuriniai/', programs_pieces_view, name='programos_kuriniai'),
    path('<int:pk>/edit/', program_edit, name='program_edit'),
    path('<int:pk>/delete/', program_delete, name='program_delete'),
    path('generuoti/', program_generate, name='program_generate'),
    path("generate-pieces/", generate_pieces, name="generate_kuriniai"),
    path("<int:ensemble_id>/", get_programs_by_ensemble, name="get_programs_by_ensemble"),

]
