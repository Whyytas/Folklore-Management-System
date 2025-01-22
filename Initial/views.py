from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class ProtectedResourceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected resource!"})

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
        return redirect('main')  # Redirect authenticated users to home
    return render(request, 'welcome.html')

class CustomLoginView(LoginView):
    template_name = '../templates/login.html'  # Path to your login template
    redirect_authenticated_user = True  # Redirect authenticated users
    success_url = reverse_lazy('main')  # Redirect URL after successful login

    def get_success_url(self):
        return self.success_url or super().get_success_url()

