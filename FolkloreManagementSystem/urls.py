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
from django.contrib import admin

from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView
from mainPage.views import (welcome, main, custom_logout, CustomLoginView,
                            manage_padaliniai, manage_ansambliai, manage_nariai)


urlpatterns = [
    path('', welcome, name='welcome'),  # Root URL points to the welcome page
    path("admin/", admin.site.urls),
    #path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    #path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include("apis.urls")),
    path('main/', include('mainPage.urls')),  # Include app-specific URLs
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('logout/', custom_logout, name='logout'),  # Logout pag

    path('', welcome, name='welcome'),

    #APIS
    path('padaliniai/<int:id>/', manage_padaliniai, name='padaliniai-detail'),
    path('padaliniai/', manage_padaliniai, name='padaliniai'),
    path('ansambliai/<int:id>/', manage_ansambliai, name='ansambliai-detail'),
    path('ansambliai/', manage_ansambliai, name='ansambliai'),
    path('nariai/<int:id>/', manage_nariai, name='nariai-detail'),
    path('nariai/', manage_nariai, name='nariai'),
]

