from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PadalinysSerializer, AnsamblisSerializer, NarysSerializer
from .models import Padalinys, Ansamblis, Narys
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.models import AccessToken
from rest_framework import status
from .permissions import IsAdminOrReadOnly, IsAdminOrModeratorOrReadOnly, IsAdminOnly


class PadalinysViewSet(viewsets.ModelViewSet):
    queryset = Padalinys.objects.all()
    serializer_class = PadalinysSerializer
    permission_classes = [IsAuthenticated, IsAdminOrModeratorOrReadOnly]


class AnsamblisViewSet(viewsets.ModelViewSet):
    queryset = Ansamblis.objects.all()
    serializer_class = AnsamblisSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class NarysViewSet(viewsets.ModelViewSet):
    """
    A viewset for Narys where only admins have access.
    """
    queryset = Narys.objects.all()
    serializer_class = NarysSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]


class LogoutView(APIView):
    """
    Revoke the access and refresh tokens to log the user out.
    """

    def post(self, request, *args, **kwargs):
        token = request.POST.get('token', None)
        if not token:
            return Response(
                {"error": "invalid_request", "error_description": "Missing token parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            access_token = AccessToken.objects.get(token=token)
            access_token.delete()  # Revoke the token by deleting it
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except AccessToken.DoesNotExist:
            return Response(
                {"error": "invalid_token", "error_description": "The provided token does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
