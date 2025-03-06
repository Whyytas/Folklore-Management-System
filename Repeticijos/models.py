from django.db import models
from Kuriniai.models import Kurinys  # Import Kūriniai model

class Repeticija(models.Model):
    pavadinimas = models.CharField(max_length=255)
    data = models.DateTimeField()  # 🔥 Change from DateField to DateTimeField
    kuriniai = models.ManyToManyField(Kurinys, related_name='repeticijos')

    def __str__(self):
        return f"{self.pavadinimas} ({self.data.strftime('%Y-%m-%d %H:%M')})"  # ✅ Format properly
