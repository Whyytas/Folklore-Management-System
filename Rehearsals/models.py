from django.db import models
from Pieces.models import Piece
from Ensembles.models import Ensemble  # 🔥 Import Ansamblis model

class Rehearsal(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()  #  DateTimeField to store both date and time
    pieces = models.ManyToManyField(Piece, through='RehearsalPiece')
    ensemble = models.ForeignKey(Ensemble, on_delete=models.CASCADE, related_name='rehearsals')  #  Multiple Ansamblis
    created = models.DateTimeField(auto_now_add=True)  #  Automatically set on creation

    def __str__(self):
        if self.date:
            return f"{self.title} ({self.date.strftime('%Y-%m-%d %H:%M')})"
        return "Nėra"

class RehearsalPiece(models.Model):
    rehearsal = models.ForeignKey('Rehearsal', on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('rehearsal', 'piece')
        ordering = ['order']