# forms.py
from django import forms
from .models import Kurinys

class KurinysForm(forms.ModelForm):
    class Meta:
        model = Kurinys
        fields = "__all__"
