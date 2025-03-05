from django.db import models
from Kuriniai.models import *  # Import Kūriniai model

class Repeticija(models.Model):
    pavadinimas = models.CharField(max_length=255)
    data = models.DateField()
    kuriniai = models.ManyToManyField(Kurinys, related_name='repeticijos')

    def __str__(self):
        return f"{self.pavadinimas} ({self.data})"
