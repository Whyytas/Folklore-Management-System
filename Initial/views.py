from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
def custom_logout(request):
    """
    Custom logout view that supports both GET and POST requests.
    """
    logout(request)  # Log out the user
    return redirect('/')  # Redirect to the login page

class CustomLoginView(LoginView):
    template_name = '../templates/login.html'  # Path to your login template
    redirect_authenticated_user = True  # Redirect authenticated users
    success_url = reverse_lazy('main')  # Redirect URL after successful login

    def get_success_url(self):
        return self.success_url or super().get_success_url()

