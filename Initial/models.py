from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('narys', 'Narys'),
        ('vadovas', 'Vadovas'),
        ('administratorius', 'Administratorius'),
    ]

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='narys')

    def __str__(self):
        return self.username
