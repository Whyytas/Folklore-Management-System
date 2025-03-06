from django import forms
from .models import Kurinys

class KurinysForm(forms.ModelForm):
    class Meta:
        model = Kurinys
        fields = ['pavadinimas', 'tipas', 'trukme', 'youtube_url', 'lyrics']
        widgets = {
            'lyrics': forms.Textarea(attrs={'rows': 5, 'style': 'display: none;'})  # Initially hidden
        }
