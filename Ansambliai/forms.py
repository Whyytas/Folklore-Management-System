from django import forms
from .models import Ansamblis

class AnsamblisForm(forms.ModelForm):
    class Meta:
        model = Ansamblis
        fields = ['pavadinimas', 'miestas']
