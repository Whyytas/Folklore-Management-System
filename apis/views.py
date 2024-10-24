from rest_framework import viewsets
from .serializers import PadalinysSerializer, AnsamblisSerializer, NarysSerializer
from .models import Padalinys, Ansamblis, Narys
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PadalinysViewSet(viewsets.ModelViewSet):
    queryset = Padalinys.objects.all()
    serializer_class = PadalinysSerializer


class AnsamblisViewSet(viewsets.ModelViewSet):
    queryset = Ansamblis.objects.all()
    serializer_class = AnsamblisSerializer

class NarysViewSet(viewsets.ModelViewSet):
    queryset = Narys.objects.all()
    serializer_class = NarysSerializer
