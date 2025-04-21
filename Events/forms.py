from django import forms
from .models import Event, Ensemble, Program

class EventForm(forms.ModelForm):
    ensemble = forms.ModelChoiceField(
        queryset=Ensemble.objects.all(),
        empty_label="Pasirinkti ansamblį...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    program = forms.ModelChoiceField(
        queryset=Program.objects.all(),
        empty_label="Pasirinkti programą...",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "YYYY-MM-DD HH:MM",
            "autocomplete": "off"
        }),
        required=True
    )

    class Meta:
        model = Event
        fields = ["ensemble", "title", "address", "date", "program"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = ""  #  Force empty value
