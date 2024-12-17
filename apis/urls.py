from .views import LogoutView
from django.urls import include, path
from rest_framework import routers
from .views import PadalinysViewSet, AnsamblisViewSet, NarysViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="My Folklore APIs",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'api/padaliniai', PadalinysViewSet)
router.register(r'api/ansambliai', AnsamblisViewSet)
router.register(r'api/nariai', NarysViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
