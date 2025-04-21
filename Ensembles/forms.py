from django import forms
from .models import Ensemble

class EnsembleForm(forms.ModelForm):
    class Meta:
        model = Ensemble
        fields = ['title', 'city', 'department']  # include padalinys
