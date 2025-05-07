# scripts/populate_sutartines_pieces.py
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FolkloreManagementSystem.settings')  # change this!
django.setup()

from Ensembles.models import Ensemble
from Pieces.models import Piece, Feature  # adjust if your app name is different

PIECES = [
    ("Anušia dukra", "1:09", "https://www.youtube.com/watch?v=U2DOkK_IRnA"),
    ("Lioj bajoroite", "1:02", "https://www.youtube.com/watch?v=xboCow7BDxw"),
    ("Lioj šokėja", "1:10", "https://www.youtube.com/watch?v=gezhgdLD4aQ"),
    ("Sese sodų sodina", "3:01", "https://www.youtube.com/watch?v=kNpy4oejbuU"),
    ("Šokinėja žvirblalis", "1:47", "https://www.youtube.com/watch?v=DiVDPsruNL0"),
    ("Unčių tupi trys pulkeliai", "0:59", "https://www.youtube.com/watch?v=nUbvZ2a5PGA"),
    ("Ažuminė Jurgelis", "2:11", "https://www.youtube.com/watch?v=e7TMc10UR-8"),
    ("Berž, berželi, berželėli", "1:17", "https://www.youtube.com/watch?v=oRqEusclhVk"),
    ("Jeglala aukštuola", "1:07", "https://www.youtube.com/watch?v=FmRK4i-S7hU"),
    ("Laduto, laduto", "3:41", "https://www.youtube.com/watch?v=axryE_pyeqQ"),
    ("Tu žilviteli, dabilia", "1:27", "https://www.youtube.com/watch?v=KqALoEgDVDY"),
    ("Tuto, strazdelis", "1:10", "https://www.youtube.com/watch?v=aASE888FjgM"),
    ("Bitele, ryto", "1:28", "https://www.youtube.com/watch?v=T0Kro0jNpaE"),
    ("Išsivedžiau oželį", "2:23", "https://www.youtube.com/watch?v=HI9O-xOfiNE"),
    ("Išvedžiau ožį", "2:10", "https://www.youtube.com/watch?v=lPYsWfp__yU"),
    ("Apvynėlis augo", "1:19", "https://www.youtube.com/watch?v=1f29dO9swwI"),
    ("Aš kanapį sėjau", "1:04", "https://www.youtube.com/watch?v=aYiC7_rctW0"),
    ("Skranc, bitele", "3:10", "https://www.youtube.com/watch?v=-ITBqOJzFWg"),
    ("Dijūta kolnali", "1:45", "https://www.youtube.com/watch?v=YN6tK-XH83U"),
    ("Kukol rože, ratilio", "3:04", "https://www.youtube.com/watch?v=-Es_qAjqOhQ"),
    ("Pijolka rūta, čiūta", "1:14", "https://www.youtube.com/watch?v=m-XPnkrIioE"),
    ("Rai lylia, ratilėli, ratilia", "1:20", "https://www.youtube.com/watch?v=VdcrkGwqRY8"),
    ("Ratui, bitela", "1:14", "https://www.youtube.com/watch?v=zJk7xeGHBuo"),
]

REGIONS = ['Aukštaitija', 'Žemaitija', 'Suvalkija', 'Dzūkija', 'Mažoji Lietuva']

def create_features():
    titles = ["Užstalės", "Vakaronei", "Susidainavimams", "Rasoms",
 "Kalėdoms", "Adventui", "Velykoms", "Pradžia"]
    for title in titles:
        Feature.objects.get_or_create(title=title)

def main():
    create_features()
    features = list(Feature.objects.all())
    ensembles = list(Ensemble.objects.all())

    for title, duration, url in PIECES:
        piece = Piece.objects.create(
            title=title,
            type="Daina",
            speed=random.choice(['Lėtas', 'Vidutinis', 'Greitas']),
            preparation=random.choice(['Naujas', 'Ruošiamas', 'Paruoštas']),
            duration=duration,
            youtube_url=url,
            description="Auto-generated from Šokame sutartines playlist.",
            region=random.choice(REGIONS)
        )

        piece.features.set(random.sample(features, 5))
        piece.ensembles.set(random.sample(ensembles, 8))

        print(f"Created: {title}")

if __name__ == "__main__":
    main()
