from django.db import models

class Padalinys(models.Model):
    pavadinimas = models.TextField()
    adresas = models.TextField()
    telNr = models.BigIntegerField()

    def __str__(self):
        return self.pavadinimas

class Ansamblis(models.Model):
    pavadinimas = models.CharField(max_length=255)
    padalinys = models.ForeignKey(Padalinys, related_name='ansambliai', on_delete=models.CASCADE)

    def __str__(self):
        return self.pavadinimas

class Narys(models.Model):  # singular naming convention
    vardas = models.CharField(max_length=255)
    pavarde = models.CharField(max_length=255)
    ansamblis = models.ForeignKey(Ansamblis, related_name='nariai', on_delete=models.CASCADE)

    def __str__(self):
        return self.vardas
