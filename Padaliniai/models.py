from django.db import models

from Ansambliai.models import Ansamblis


class Padalinys(models.Model):
    pavadinimas = models.CharField(max_length=255)
    adresas = models.TextField()
    tel_nr = models.CharField(max_length=20, default="N/A")  # Set a default value
    ansambliai = models.ManyToManyField(Ansamblis, related_name="padaliniai")
 # Ensure this field is present

    def __str__(self):
        return self.pavadinimas
