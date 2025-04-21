from django.db import models

class Department(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20, default="-")  # Set a default value
 # Ensure this field is present

    def __str__(self):
        return self.title
