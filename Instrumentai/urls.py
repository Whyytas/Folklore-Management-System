from django.urls import path
from .views import instrumentai_list, instrumentai_add, instrumentai_edit, instrumentai_delete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", instrumentai_list, name="instrumentai_list"),
    path("add/", instrumentai_add, name="instrumentai_add"),
    path("<int:pk>/edit/", instrumentai_edit, name="instrumentai_edit"),
    path("<int:pk>/delete/", instrumentai_delete, name="instrumentai_delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)