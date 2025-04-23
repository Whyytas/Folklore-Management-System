import resend
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.views import (
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetCompleteView as DjangoPasswordResetCompleteView
)

from Initial.forms import NoEmailPasswordResetForm

User = get_user_model()
resend.api_key = settings.RESEND_API_KEY

@login_required
def account_page(request):
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

    return render(request, 'account.html', {'user': user})

class CustomLoginView(auth_views.LoginView):
    """ Redirect already logged-in users to /main """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')  #  Redirect to /main if already logged in
        return super().dispatch(request, *args, **kwargs)

class ForgotPasswordView(DjangoPasswordResetView):
    form_class = NoEmailPasswordResetForm
    template_name = 'forgot_password.html'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(DjangoPasswordResetDoneView):
    template_name = 'password_reset_done.html'

class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

    def get_success_url(self):
        return reverse('password_reset_complete')

class PasswordResetCompleteView(DjangoPasswordResetCompleteView):
    template_name = 'password_reset_complete.html'