# forms.py
from django import forms
from .models import Kurinys

class KurinysForm(forms.ModelForm):
    class Meta:
        model = Kurinys
        fields = ['pavadinimas', 'tipas', 'trukme', 'youtube_url', 'lyrics', 'regionas', 'vieta', 'aprašymas', 'ansambliai']
        widgets = {
            'lyrics': forms.Textarea(attrs={
                'rows': 5,
                'style': 'display: none;',
                'class': 'form-control',
                'placeholder': 'Įveskite dainos žodžius'
            }),
            'aprašymas': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Įveskite aprašymą (neprivaloma)'
            }),
            'ansambliai': forms.CheckboxSelectMultiple(),
        }
