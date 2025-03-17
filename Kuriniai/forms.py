from django import forms
from .models import Kurinys

# forms.py
class KurinysForm(forms.ModelForm):
    class Meta:
        model = Kurinys
        fields = ['pavadinimas', 'tipas', 'trukme', 'youtube_url', 'lyrics', 'ansambliai']
        widgets = {
            'lyrics': forms.Textarea(attrs={'rows': 5, 'style': 'display: none;'}),
            'ansambliai': forms.CheckboxSelectMultiple(),  # ✅ Allow multi-select
        }
