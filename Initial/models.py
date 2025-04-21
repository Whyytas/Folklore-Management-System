from django.contrib.auth.models import AbstractUser
from django.db import models

from Ensembles.models import Ensemble


class User(AbstractUser):
    ROLE_CHOICES = [
        ('narys', 'Narys'),
        ('vadovas', 'Vadovas'),
        ('administratorius', 'Administratorius'),
    ]

    name = models.CharField(max_length=50, blank=True, null=True)  #  Add first name
    surname = models.CharField(max_length=50, blank=True, null=True)  #  Add last name
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='narys')
    ensembles = models.ManyToManyField(Ensemble, blank=True, related_name="members")

    def __str__(self):
        return f"{self.name} {self.surname} ({self.username})" if self.name and self.surname else self.username
