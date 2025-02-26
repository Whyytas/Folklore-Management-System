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
    tipas = models.CharField(max_length=50, choices=PROGRAM_TIPAS)
    aprasymas = models.TextField(blank=True, null=True)
    sukurtas = models.DateTimeField(auto_now_add=True)

class ProgramosKurinys(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    kurinys = models.ForeignKey("Kuriniai.Kurinys", on_delete=models.CASCADE)
    eile = models.PositiveIntegerField()

    class Meta:
        ordering = ["eile"]
