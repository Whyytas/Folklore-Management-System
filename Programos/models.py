from django.db import models
from datetime import timedelta

from django.db import models

class Programa(models.Model):
    PROGRAM_TIPAS = [
        ('Adventui', 'Adventui'),
        ('Rasoms', 'Rasoms'),
        ('Lygiadieniui', 'Lygiadieniui'),
        ('Vakaronei', 'Vakaronei'),
        ('Kaledoms', 'Kalėdoms'),
        ('Velykoms', 'Velykoms'),
        ('Susidainavimams', 'Susidainavimams'),
    ]
    pavadinimas = models.CharField(max_length=255)
    tipas = models.CharField(max_length=50, choices=PROGRAM_TIPAS, blank=False, null=False)
    aprasymas = models.TextField(blank=True, null=True)
    trukme = models.CharField(max_length=10, blank=True, null=True)  # ✅ User-defined trukme
    sukurtas = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pavadinimas

    def calculate_trukme(self):
        """
        Calculates the total duration of the program based on the `trukme` field
        of each associated `Kurinys` object.
        """
        total_seconds = sum(
            self._parse_trukme(pk.kurinys.trukme) for pk in self.programoskurinys_set.all()
        )

        total_minutes, seconds = divmod(total_seconds, 60)
        return f"{total_minutes:02}:{seconds:02}" if total_seconds else None

    @staticmethod
    def _parse_trukme(trukme_str):
        """
        Parses a `MM:SS` formatted string and converts it to total seconds.
        """
        if not trukme_str or ":" not in trukme_str:
            return 0
        try:
            minutes, seconds = map(int, trukme_str.split(":"))
            return minutes * 60 + seconds
        except ValueError:
            return 0


class ProgramosKurinys(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    kurinys = models.ForeignKey("Kuriniai.Kurinys", on_delete=models.CASCADE)
    eile = models.PositiveIntegerField()

    class Meta:
        ordering = ["eile"]
