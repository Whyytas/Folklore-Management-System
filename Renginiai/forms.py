from django import forms
from .models import Renginys, Ansamblis, Programa

class RenginysForm(forms.ModelForm):
    ansamblis = forms.ModelChoiceField(
        queryset=Ansamblis.objects.all(),
        empty_label="Pasirinkti ansamblį...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    programa = forms.ModelChoiceField(
        queryset=Programa.objects.all(),
        empty_label="Pasirinkti programą...",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    data_laikas = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "YYYY-MM-DD HH:MM",
            "autocomplete": "off"
        }),
        required=True
    )

    class Meta:
        model = Renginys
        fields = ["ansamblis", "pavadinimas", "adresas", "data_laikas", "programa"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["data_laikas"].initial = ""  # ✅ Force empty value
