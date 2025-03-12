import os
from django.db import models
from django.utils.text import slugify

def instrumentas_image_upload_path(instance, filename):
    """
    Rename the uploaded image using the format: ansamblis-instrumento_pavadinimas.jpg
    """
    # Ensure ansamblis and instrumentas name are safe for filenames
    ansamblis_name = slugify(instance.ansamblis.pavadinimas)
    instrumentas_name = slugify(instance.pavadinimas)

    # Construct new filename
    new_filename = f"{ansamblis_name}-{instrumentas_name}.jpg"

    # Ensure the image is saved in "instrument_photos/" directory
    return os.path.join("instrument_photos/", new_filename)

class Instrumentas(models.Model):
    pavadinimas = models.CharField(max_length=255)
    nuotrauka = models.ImageField(upload_to=instrumentas_image_upload_path, blank=True, null=True)  # ✅ Renames image before saving
    ansamblis = models.ForeignKey("Ansambliai.Ansamblis", on_delete=models.CASCADE, related_name="instrumentai")

    def __str__(self):
        return self.pavadinimas
