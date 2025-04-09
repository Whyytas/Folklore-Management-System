from django.db import models

class Padalinys(models.Model):
    pavadinimas = models.CharField(max_length=255)
    adresas = models.TextField()
    tel_nr = models.CharField(max_length=20, default="-")  # Set a default value
 # Ensure this field is present

    def __str__(self):
        return self.pavadinimas
