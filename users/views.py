from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('/')
# Create your views here.


