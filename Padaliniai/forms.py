from django import forms
from .models import Padalinys

class PadalinysForm(forms.ModelForm):
    class Meta:
        model = Padalinys
        fields = ["pavadinimas", "adresas", "tel_nr"]
        widgets = {
            "pavadinimas": forms.TextInput(attrs={"class": "form-control"}),
            "adresas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "tel_nr": forms.TextInput(attrs={"class": "form-control"}),
        }
