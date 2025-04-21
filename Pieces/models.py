# models.py
from django.db import models
from Ensembles.models import Ensemble

class Feature(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Piece(models.Model):
    TITLE_MAX_LENGTH = 255
    TYPE_CHOICES = [
        ('Daina', 'Daina'),
        ('Šokis', 'Šokis'),
        ('Kapela', 'Kapela'),
        ('Instrumentalas', 'Instrumentalas'),
    ]
    SPEED_CHOICES = [
        ('Lėtas', 'Lėtas'),
        ('Vidutinis', 'Vidutinis'),
        ('Greitas', 'Greitas'),
    ]
    PREPARATION_CHOICES = [
        ('Naujas', 'Naujas'),
        ('Ruošiamas', 'Ruošiamas'),
        ('Paruoštas', 'Paruoštas'),
        ('Archyvas', 'Archyvas'),
    ]

    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    speed = models.CharField(max_length=20, choices=SPEED_CHOICES, blank=True, null=True)
    preparation = models.CharField(max_length=20, choices=PREPARATION_CHOICES, default='Naujas')
    duration = models.CharField(max_length=10, blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  #  Description field
    notes = models.FileField(upload_to='natos/', blank=True, null=True)
    notes_image = models.ImageField(upload_to='natos_images/', blank=True, null=True)
    region = models.CharField(
        max_length=20,
        choices=[('Aukštaitija', 'Aukštaitija'),
                 ('Žemaitija', 'Žemaitija'),
                 ('Dzūkija', 'Dzūkija'),
                 ('Suvalkija', 'Suvalkija'),
                 ('Mažoji Lietuva', 'Mažoji Lietuva')],
        blank=True, null=True
    )
    place = models.CharField(max_length=100, blank=True, null=True)
    ensembles = models.ManyToManyField(Ensemble)
    features = models.ManyToManyField(Feature, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

