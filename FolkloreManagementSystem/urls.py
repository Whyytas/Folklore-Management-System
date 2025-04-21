"""
URL configuration for FolkloreManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.auth.views import redirect_to_login
from django.urls import include, path
# from Initial.views import (custom_logout, CustomLoginView,)
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from Initial.views import CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('main/', include('mainPage.urls')),  # Include app-specific URLs
    path('', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout pag
    path('', include('Initial.urls')),
    path('ansambliai/', include('Ensembles.urls')),
    path('nariai/', include('Users.urls')),
    path('renginiai/', include('Events.urls')),
    path('kuriniai/', include('Pieces.urls')),
    path('programos/', include('Programs.urls')),
    path('instrumentai/', include('Instruments.urls')),
    path('padaliniai/', include('Departments.urls')),
    path('paskyra/', include('Users.urls')),
    path('repeticijos/', include('Rehearsals.urls')),
    path('kalendorius/', include('Calendar.urls')),

] + debug_toolbar_urls()

