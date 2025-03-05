from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import views as auth_views

User = get_user_model()

@login_required
def paskyra_page(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')

        if username:
            user.username = username
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number
        if role in dict(User.ROLE_CHOICES):
            user.role = role

        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('paskyra')

    return render(request, 'paskyra.html', {'user': user})

class CustomLoginView(auth_views.LoginView):
    """ Redirect already logged-in users to /main """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')  # ✅ Redirect to /main if already logged in
        return super().dispatch(request, *args, **kwargs)
