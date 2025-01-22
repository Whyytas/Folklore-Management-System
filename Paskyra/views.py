from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

@login_required
def paskyra_page(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('paskyra')
        else:
            messages.error(request, 'Both username and email are required.')

    return render(request, 'paskyra.html', {'user': user})
