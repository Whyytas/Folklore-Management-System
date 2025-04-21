from django import forms
from .models import Instrument

class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ['title', 'photo', 'ensemble']

    #  Ensure file uploads are handled properly
    photo = forms.ImageField(required=False)
