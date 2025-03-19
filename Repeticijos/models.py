from django.db import models
from Kuriniai.models import Kurinys
from Ansambliai.models import Ansamblis  # 🔥 Import Ansamblis model

class Repeticija(models.Model):
    pavadinimas = models.CharField(max_length=255)
    data = models.DateTimeField()  # ✅ DateTimeField to store both date and time
    kuriniai = models.ManyToManyField(Kurinys, through='RepeticijaKurinys')
    ansamblis = models.ForeignKey(Ansamblis, on_delete=models.CASCADE, related_name='repeticijos')  # ✅ Multiple Ansamblis
    created = models.DateTimeField(auto_now_add=True)  # ✅ Automatically set on creation

    def __str__(self):
        if self.data:
            return f"{self.pavadinimas} ({self.data.strftime('%Y-%m-%d %H:%M')})"
        return "Nėra"

class RepeticijaKurinys(models.Model):
    repeticija = models.ForeignKey('Repeticija', on_delete=models.CASCADE)
    kurinys = models.ForeignKey(Kurinys, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('repeticija', 'kurinys')
        ordering = ['order']