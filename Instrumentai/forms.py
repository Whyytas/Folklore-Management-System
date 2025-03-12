from django import forms
from .models import Instrumentas

class InstrumentasForm(forms.ModelForm):
    class Meta:
        model = Instrumentas
        fields = ['pavadinimas', 'nuotrauka', 'ansamblis']

    # ✅ Ensure file uploads are handled properly
    nuotrauka = forms.ImageField(required=False)
