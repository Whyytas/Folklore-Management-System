from django import forms

from Kuriniai.models import Kurinys
from .models import Repeticija

class RepeticijaForm(forms.ModelForm):
    kuriniai = forms.ModelMultipleChoiceField(
        queryset=Kurinys.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Repeticija
        fields = ['pavadinimas', 'data', 'kuriniai']
