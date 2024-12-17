from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apis.models import Padalinys, Ansamblis, Narys

class CustomLoginView(LoginView):
    template_name = '../templates/login.html'  # Path to your login template
    redirect_authenticated_user = True  # Redirect authenticated users
    success_url = reverse_lazy('main')  # Redirect URL after successful login

    def get_success_url(self):
        return self.success_url or super().get_success_url()

@login_required
def main(request):
    """
    main page view that displays content based on the user's role.
    """
    user_role = getattr(request.user, 'role', None)

    # Default context for all users
    context = {
        'user_role': user_role,
        'ansambliai': Ansamblis.objects.all() if user_role in ['admin', 'moderator', 'user'] else None,
        'padaliniai': Padalinys.objects.all() if user_role in ['admin', 'moderator', 'user'] else None,
        'nariai': Narys.objects.all() if user_role in ['admin', 'moderator'] else None,
    }

    return render(request, 'main.html', context)

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    """
    Custom logout view that supports both GET and POST requests.
    """
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page

def welcome(request):
    """
    Welcome page view.
    If the user is authenticated, redirect them to the home page.
    Otherwise, redirect to the login page.
    """
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to home
    return render(request, 'welcome.html')  # Render the welcome page for unauthenticated users

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apis.models import Padalinys
import json

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