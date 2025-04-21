from django import forms
from django.contrib.auth.forms import UserCreationForm
from Initial.models import User  #  Ensure correct model is imported

class UserCreateForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'role', 'password1', 'password2']
