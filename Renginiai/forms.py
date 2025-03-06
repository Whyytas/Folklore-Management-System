from django import forms
from .models import Renginys, Ansamblis, Programa
from django.utils.timezone import localtime

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

    data_laikas = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
        input_formats=["%Y-%m-%dT%H:%M"],  # ✅ Lithuanian format enforced
    )

    class Meta:
        model = Renginys
        fields = ["ansamblis", "pavadinimas", "adresas", "data_laikas", "programa"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["data_laikas"].initial = localtime(self.instance.data_laikas).strftime("%Y-%m-%dT%H:%M")
