# models.py
from django.db import models
from Ansambliai.models import Ansamblis

class Kurinys(models.Model):
    PAVADINIMAS_MAX_LENGTH = 255
    TIPAS_CHOICES = [
        ('Daina', 'Daina'),
        ('Šokis', 'Šokis'),
        ('Kapela', 'Kapela'),
    ]

    pavadinimas = models.CharField(max_length=PAVADINIMAS_MAX_LENGTH)
    tipas = models.CharField(max_length=20, choices=TIPAS_CHOICES)
    trukme = models.CharField(max_length=10, blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    aprašymas = models.TextField(blank=True, null=True)  # ✅ Description field
    regionas = models.CharField(
        max_length=20,
        choices=[('Aukštaitija', 'Aukštaitija'), ('Žemaitija', 'Žemaitija'),
                 ('Dzūkija', 'Dzūkija'), ('Suvalkija', 'Suvalkija'),
                 ('Mažoji Lietuva', 'Mažoji Lietuva')],
        blank=True, null=True
    )
    vieta = models.CharField(max_length=100, blank=True, null=True)
    ansambliai = models.ManyToManyField(Ansamblis)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pavadinimas
