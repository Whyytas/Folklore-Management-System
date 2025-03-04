from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()

@login_required
def nariai_list(request):
    users = User.objects.all()  # Get all users
    return render(request, 'nariai.html', {'users': users})


# ✅ Custom Form for Creating a User
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('narys', 'Narys'),
        ('vadovas', 'Vadovas'),
        ('administratorius', 'Administratorius'),
    ]

    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

# ✅ View to Add a New User
@login_required
def nariai_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Naujas vartotojas sėkmingai pridėtas!")
            return redirect('nariai')  # ✅ Redirect to user list after success
        else:
            messages.error(request, "Klaida: Patikrinkite formą ir bandykite dar kartą.")  # ✅ Show errors

    else:
        form = CustomUserCreationForm()

    return render(request, 'nariai_add.html', {'form': form})

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

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Vartotojas sėkmingai atnaujintas!")
            return redirect('nariai')  # Redirect back to user list
        else:
            messages.error(request, "Klaida: Nepavyko atnaujinti vartotojo.")
    else:
        form = CustomUserEditForm(instance=user)

    return render(request, 'nariai_edit.html', {'form': form, 'user': user})

@login_required
def nariai_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "Vartotojas sėkmingai ištrintas.")
        return redirect('nariai')  # Redirect to user list

    messages.error(request, "Negalima ištrinti vartotojo.")
    return redirect('nariai')
