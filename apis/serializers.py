from rest_framework import serializers
from .models import Padalinys, Ansamblis, Narys

class PadalinysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Padalinys
        fields = ('id', 'pavadinimas', 'adresas', 'telNr')  # Add 'id' field

class AnsamblisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ansamblis
        fields = ('id', 'pavadinimas', 'padalinys')  # Add 'id' field

class NarysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Narys
        fields = ('id', 'vardas', 'pavarde', 'ansamblis')  # Add 'id' field
