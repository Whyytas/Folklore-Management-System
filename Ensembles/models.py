from django.db import models
from Departments.models import Department

class Ensemble(models.Model):
    title = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="ensembles", blank=True, null=True)

    def __str__(self):
        return self.title
