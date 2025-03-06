from django.db import models

class Kurinys(models.Model):
    PAVADINIMAS_MAX_LENGTH = 255
    TIPAS_CHOICES = [
        ('Daina', 'Daina'),
        ('Šokis', 'Šokis'),
        ('Kapela', 'Kapela'),
    ]

    pavadinimas = models.CharField(max_length=PAVADINIMAS_MAX_LENGTH)
    tipas = models.CharField(max_length=20, choices=TIPAS_CHOICES, blank=False, null=False)
    trukme = models.CharField(max_length=10, blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)  # ✅ Optional lyrics field

    def __str__(self):
        return self.pavadinimas
