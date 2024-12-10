from .views import LogoutView
from django.urls import include, path
from rest_framework import routers
from .views import PadalinysViewSet, AnsamblisViewSet, NarysViewSet

router = routers.DefaultRouter()
router.register(r'padaliniai', PadalinysViewSet)
router.register(r'ansambliai', AnsamblisViewSet)
router.register(r'nariai', NarysViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]
