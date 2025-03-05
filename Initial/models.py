from django.contrib.auth.models import AbstractUser
from django.db import models

from Ansambliai.models import Ansamblis


class User(AbstractUser):
    ROLE_CHOICES = [
        ('narys', 'Narys'),
        ('vadovas', 'Vadovas'),
        ('administratorius', 'Administratorius'),
    ]

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='narys')
    ansambliai = models.ManyToManyField(Ansamblis, blank=True, related_name="members")

    def __str__(self):
        return self.username
