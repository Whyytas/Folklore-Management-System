from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

class Padalinys(models.Model):
    pavadinimas = models.TextField()
    adresas = models.TextField()
    telNr = models.BigIntegerField()

    def __str__(self):
        return self.pavadinimas
