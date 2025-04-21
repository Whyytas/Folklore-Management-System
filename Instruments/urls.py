from django.urls import path
from .views import instruments_list, instrument_add, instrument_edit, instrument_delete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", instruments_list, name="instrumentai_list"),
    path("add/", instrument_add, name="instrumentai_add"),
    path("<int:pk>/edit/", instrument_edit, name="instrumentai_edit"),
    path("<int:pk>/delete/", instrument_delete, name="instrumentai_delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)