import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FolkloreManagementSystem.settings")
django.setup()

import random
from Pieces.models import Piece, Feature
from Ensembles.models import Ensemble

TYPE_CHOICES = ['Daina', 'Šokis', 'Kapela', 'Instrumentalas']
SPEED_CHOICES = ['Lėtas', 'Vidutinis', 'Greitas']
PREPARATION_CHOICES = ['Naujas', 'Ruošiamas', 'Paruoštas', 'Archyvas']
REGION_CHOICES = ['Aukštaitija', 'Žemaitija', 'Dzūkija', 'Suvalkija', 'Mažoji Lietuva']

ensemble = Ensemble.objects.get(id=1)
features = list(Feature.objects.all())

for i in range(50):
    piece = Piece.objects.create(
        title=f"Piece A1-{i+1}",
        type=random.choice(TYPE_CHOICES),
        speed=random.choice(SPEED_CHOICES),
        preparation=random.choice(PREPARATION_CHOICES),
        duration=f"{random.randint(1, 4)}:{random.randint(0, 59):02}",
        youtube_url=f"https://youtube.com/watch?v=a1p{i+1}",
        lyrics=f"Lyrics for Piece A1-{i+1}",
        description=f"Description for Piece A1-{i+1}",
        region=random.choice(REGION_CHOICES),
        place=f"Place {random.randint(1, 100)}"
    )
    piece.ensembles.add(ensemble)

    if features:
        piece.features.set(random.sample(features, k=random.randint(0, min(3, len(features)))))

print(" Created 50 pieces for Ensemble ID 1.")
