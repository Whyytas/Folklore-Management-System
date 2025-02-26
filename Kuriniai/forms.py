from django import forms
from .models import Kurinys

class KurinysForm(forms.ModelForm):
    class Meta:
        model = Kurinys
        fields = ['pavadinimas', 'tipas', 'trukme', 'youtube_url']

    tipas = forms.ChoiceField(choices=Kurinys.TIPAS_CHOICES, required=True)
