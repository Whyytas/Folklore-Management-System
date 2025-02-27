from django.db import models

from Ansambliai.models import Ansamblis


class Instrumentas(models.Model):
    pavadinimas = models.CharField(max_length=255)
    nuotrauka = models.URLField(blank=True, null=True)
    ansamblis = models.ForeignKey(Ansamblis, on_delete=models.CASCADE, related_name="instrumentai")

    def __str__(self):
        return self.pavadinimas
