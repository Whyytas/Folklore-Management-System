from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from Ansambliai.models import Ansamblis

from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)



User = get_user_model()  # ✅ Ensure you're using the correct model


@login_required
def nariai_list(request):
    users = User.objects.all()  # Get all users
    return render(request, 'nariai.html', {'users': users})


# ✅ Custom Form for Creating a User
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    ansambliai = forms.ModelMultipleChoiceField(
        queryset=Ansamblis.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # ✅ Ensure Django accepts multiple values
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role', 'password1', 'password2', 'ansambliai']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
# ✅ View to Add a New User
@login_required
def nariai_add(request):
    all_ansambliai = Ansamblis.objects.all()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        logger.debug(f"Received POST data: {request.POST}")  # ✅ Log received form data

        if form.is_valid():
            user = form.save(commit=False)
            user.save()  # ✅ Save the user first

            # ✅ Debugging: Check what is being received
            selected_ansambliai_ids = request.POST.getlist("ansambliai")  # ✅ Retrieve as list
            logger.debug(f"Selected Ansambliai IDs: {selected_ansambliai_ids}")

            try:
                if selected_ansambliai_ids:
                    selected_ansambliai = Ansamblis.objects.filter(id__in=selected_ansambliai_ids)
                    user.ansambliai.set(selected_ansambliai)  # ✅ Assign ansambliai
                else:
                    user.ansambliai.clear()  # ✅ Clear if no selection

                messages.success(request, "Naujas vartotojas sėkmingai pridėtas!")
                return redirect('nariai')

            except Exception as e:
                logger.error(f"Error setting ansambliai: {e}")
                messages.error(request, f"Klaida priskiriant ansamblius: {e}")

        else:
            messages.error(request, "Klaida: Patikrinkite formą ir bandykite dar kartą.")
            logger.error(f"Form errors: {form.errors}")

    else:
        form = CustomUserCreationForm()

    return render(request, 'nariai_add.html', {'form': form, 'all_ansambliai': all_ansambliai})



@login_required
def nariai_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'nariai_view.html', {'user': user})

# ✅ Custom User Edit Form
class CustomUserEditForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('narys', 'Narys'),
        ('vadovas', 'Vadovas'),
        ('administratorius', 'Administratorius'),
    ]

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

# ✅ View to Edit a User
@login_required
def nariai_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    all_ansambliai = Ansamblis.objects.all()

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.role = request.POST.get('role')

        selected_ansambliai = request.POST.getlist('ansambliai')
        user.ansambliai.set(Ansamblis.objects.filter(id__in=selected_ansambliai))

        user.save()
        messages.success(request, "Vartotojas atnaujintas sėkmingai.")
        return redirect('nariai')

    return render(request, 'nariai_edit.html', {'user': user, 'all_ansambliai': all_ansambliai})

@login_required
def nariai_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "Vartotojas sėkmingai ištrintas.")
        return redirect('nariai')  # Redirect to user list

    messages.error(request, "Negalima ištrinti vartotojo.")
    return redirect('nariai')
