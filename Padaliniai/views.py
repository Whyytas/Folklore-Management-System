from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import PadalinysSerializer
from .models import Padalinys
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.models import AccessToken
from rest_framework import status
from .permissions import IsAdminOrModeratorOrReadOnly
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render

# Create your views here.
class PadalinysViewSet(viewsets.ModelViewSet):
    queryset = Padalinys.objects.all()
    serializer_class = PadalinysSerializer
    permission_classes = [IsAuthenticated, IsAdminOrModeratorOrReadOnly]

def manage_padaliniai(request, id=None):
    """
    Handle all CRUD operations for Padaliniai.
    """
    if request.method == "GET":
        # Fetch and render all Padaliniai
        padaliniai = Padalinys.objects.all()
        return render(request, 'padaliniai.html', {'padaliniai': padaliniai})

    elif request.method == "POST" and id is None:
        # Create new Padalinys
        try:
            data = json.loads(request.body)
            Padalinys.objects.create(
                pavadinimas=data["pavadinimas"],
                adresas=data["adresas"],
                telNr=data["telNr"],
            )
            return JsonResponse({"success": True, "message": "Padalinys created successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    elif request.method == "PUT" and id:
        # Update existing Padalinys
        try:
            padalinys = get_object_or_404(Padalinys, id=id)
            data = json.loads(request.body)
            padalinys.pavadinimas = data.get("pavadinimas", padalinys.pavadinimas)
            padalinys.adresas = data.get("adresas", padalinys.adresas)
            padalinys.telNr = data.get("telNr", padalinys.telNr)
            padalinys.save()
            return JsonResponse({"success": True, "message": "Padalinys updated successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    elif request.method == "DELETE" and id:
        # Delete an existing Padalinys
        try:
            padalinys = get_object_or_404(Padalinys, id=id)
            padalinys.delete()
            return JsonResponse({"success": True, "message": "Padalinys deleted successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid HTTP method or missing ID."})

