# from time import localtime
from django.utils.timezone import localtime, is_naive, make_aware

from django.db import models

from Ansambliai.models import Ansamblis
from Programos.models import Programa


class Renginys(models.Model):
    ansamblis = models.ForeignKey(Ansamblis, on_delete=models.CASCADE)
    pavadinimas = models.CharField(max_length=255)
    adresas = models.TextField()
    data_laikas = models.DateTimeField()
    programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ One-to-Many
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_data_laikas(self):
        dt = self.data_laikas
        if is_naive(dt):
            dt = make_aware(dt)
        return localtime(dt).strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        return f"{self.pavadinimas} ({self.ansamblis})"