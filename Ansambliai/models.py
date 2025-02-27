from django.db import models


class Ansamblis(models.Model):
    pavadinimas = models.CharField(max_length=255)
    miestas = models.CharField(max_length=255)

    def __str__(self):
        return self.pavadinimas