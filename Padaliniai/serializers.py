from rest_framework import serializers
from .models import Padalinys
class PadalinysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Padalinys
        fields = ('id', 'pavadinimas', 'adresas', 'telNr')  # Add 'id' field