# from time import localtime
from django.utils.timezone import localtime, is_naive, make_aware

from django.db import models

from Ensembles.models import Ensemble
from Programs.models import Program


class Event(models.Model):
    ensemble = models.ForeignKey(Ensemble, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    address = models.TextField()
    date = models.DateTimeField()
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)  #  One-to-Many
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_data_laikas(self):
        dt = self.date
        if is_naive(dt):
            dt = make_aware(dt)
        return localtime(dt).strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        return f"{self.title} ({self.ensemble})"