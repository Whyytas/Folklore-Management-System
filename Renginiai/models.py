from django.db import models

class Renginys(models.Model):
    ansamblis = models.ForeignKey('Ansambliai.Ansamblis', on_delete=models.CASCADE)  # ✅ Cross-app reference
    pavadinimas = models.CharField(max_length=255)
    adresas = models.TextField()
    data_laikas = models.DateTimeField()

    def __str__(self):
        return f"{self.pavadinimas} ({self.ansamblis})"
