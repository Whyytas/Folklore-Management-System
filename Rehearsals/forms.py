from django import forms

from Pieces.models import Piece
from .models import Rehearsal

class RehearsalForm(forms.ModelForm):
    pieces = forms.ModelMultipleChoiceField(
        queryset=Piece.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Rehearsal
        fields = ['title', 'date', 'pieces']
