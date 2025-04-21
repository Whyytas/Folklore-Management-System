import os
from django.db import models
from django.utils.text import slugify

def instrumentas_image_upload_path(instance, filename):
    """
    Rename the uploaded image using the format: ansamblis-instrumento_pavadinimas.jpg
    """
    # Ensure ansamblis and instrumentas name are safe for filenames
    ensemble_name = slugify(instance.ensemble.title)
    instrument_name = slugify(instance.title)

    # Construct new filename
    new_filename = f"{ensemble_name}-{instrument_name}.jpg"

    # Ensure the image is saved in "instrument_photos/" directory
    return os.path.join("instrument_photos/", new_filename)

class Instrument(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=instrumentas_image_upload_path, blank=True, null=True)  #  Renames image before saving
    ensemble = models.ForeignKey("Ensembles.Ensemble", on_delete=models.CASCADE, related_name="instrumentai")

    def __str__(self):
        return self.title
