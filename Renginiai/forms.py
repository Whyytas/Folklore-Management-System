from django import forms
from .models import Renginys
from Ansambliai.models import Ansamblis  # ✅ Import from the other app

class RenginysForm(forms.ModelForm):
    ansamblis = forms.ModelChoiceField(
        queryset=Ansamblis.objects.all(),
        empty_label="Pasirinkti ansamblį...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Renginys
        fields = ['ansamblis', 'pavadinimas', 'adresas', 'data_laikas']
