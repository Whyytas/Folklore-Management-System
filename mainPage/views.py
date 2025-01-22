from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    """
    main page view that displays content based on the user's role.
    """
    user_role = getattr(request.user, 'role', None)

    return render(request, 'main.html')


