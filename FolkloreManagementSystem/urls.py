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
from Initial.views import (welcome, custom_logout, CustomLoginView,)


urlpatterns = [
    path('', welcome, name='welcome'),  # Root URL points to the welcome page
    path("admin/", admin.site.urls),

    path('main/', include('mainPage.urls')),  # Include app-specific URLs
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('logout/', custom_logout, name='logout'),  # Logout pag

    path('ansambliai/', include('Ansambliai.urls')),
    path('nariai/', include('Nariai.urls')),
    path('renginiai/', include('Renginiai.urls')),
]

