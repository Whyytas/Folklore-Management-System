# ansambliai/models.py
from django.db import models
from Padaliniai.models import Padalinys


class Ansamblis(models.Model):
    pavadinimas = models.CharField(max_length=255)
    miestas = models.CharField(max_length=255)
    padalinys = models.ForeignKey(Padalinys, on_delete=models.PROTECT, related_name="ansambliai", blank=True, null=True)

    def __str__(self):
        return self.pavadinimas
