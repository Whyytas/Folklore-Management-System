from django import forms
from .models import Department

class UnitForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["title", "address", "phone"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
