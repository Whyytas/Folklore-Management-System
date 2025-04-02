# models.py
from django.db import models
from Ansambliai.models import Ansamblis

class Pozymis(models.Model):
    pavadinimas = models.CharField(max_length=100)

    def __str__(self):
        return self.pavadinimas

class Kurinys(models.Model):
    PAVADINIMAS_MAX_LENGTH = 255
    TIPAS_CHOICES = [
        ('Daina', 'Daina'),
        ('Šokis', 'Šokis'),
        ('Kapela', 'Kapela'),
        ('Instrumentalas', 'Instrumentalas'),
    ]
    GREITUMAS_CHOICES = [
        ('Lėtas', 'Lėtas'),
        ('Vidutinis', 'Vidutinis'),
        ('Greitas', 'Greitas'),
    ]
    PARUOSIMAS_CHOICES = [
        ('Naujas', 'Naujas'),
        ('Ruošiamas', 'Ruošiamas'),
        ('Paruoštas', 'Paruoštas'),
        ('Archyvas', 'Archyvas'),
    ]

    pavadinimas = models.CharField(max_length=PAVADINIMAS_MAX_LENGTH)
    tipas = models.CharField(max_length=20, choices=TIPAS_CHOICES)
    greitumas = models.CharField(max_length=20, choices=GREITUMAS_CHOICES, blank=True, null=True)
    paruosimas = models.CharField(max_length=20, choices=PARUOSIMAS_CHOICES, default='Naujas')
    trukme = models.CharField(max_length=10, blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    aprasymas = models.TextField(blank=True, null=True)  # ✅ Description field
    natos = models.FileField(upload_to='natos/', blank=True, null=True)
    natos_image = models.ImageField(upload_to='natos_images/', blank=True, null=True)
    regionas = models.CharField(
        max_length=20,
        choices=[('Aukštaitija', 'Aukštaitija'),
                 ('Žemaitija', 'Žemaitija'),
                 ('Dzūkija', 'Dzūkija'),
                 ('Suvalkija', 'Suvalkija'),
                 ('Mažoji Lietuva', 'Mažoji Lietuva')],
        blank=True, null=True
    )
    vieta = models.CharField(max_length=100, blank=True, null=True)
    ansambliai = models.ManyToManyField(Ansamblis)
    pozymiai = models.ManyToManyField(Pozymis, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pavadinimas

