from django.db import models
from datetime import timedelta

from django.db import models

from Ensembles.models import Ensemble


class Program(models.Model):
    PROGRAM_TYPE = [
        ('Adventui', 'Adventui'),
        ('Rasoms', 'Rasoms'),
        ('Lygiadieniui', 'Lygiadieniui'),
        ('Vakaronei', 'Vakaronei'),
        ('Kaledoms', 'Kalėdoms'),
        ('Velykoms', 'Velykoms'),
        ('Susidainavimams', 'Susidainavimams'),
    ]
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=PROGRAM_TYPE, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)  #  User-defined trukme
    created = models.DateTimeField(auto_now_add=True)
    ensemble = models.ForeignKey(Ensemble, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class ProgramPiece(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    piece = models.ForeignKey("Pieces.Piece", on_delete=models.CASCADE)
    queue = models.PositiveIntegerField()

    class Meta:
        ordering = ["queue"]
