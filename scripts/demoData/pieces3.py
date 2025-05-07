# scripts/populate_ratilio_instrumentals.py
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FolkloreManagementSystem.settings')  # Replace this
django.setup()

from Ensembles.models import Ensemble
from Pieces.models import Piece, Feature

PIECES = [
    ("Atėjo šiltas pavasarėlis", "3:45", "https://www.youtube.com/watch?v=c6WIFs8RdoY"),
    ("Menu pavasarį neramų", "3:24", "https://www.youtube.com/watch?v=tnXSd3AjO1w"),
    ("Paulausko valsas", "2:37", "https://www.youtube.com/watch?v=60DUh_Ak93c"),
    ("Giesmė „Pone Karaliau“", "5:09", "https://www.youtube.com/watch?v=V3nitiGk2LA"),
    ("Viduj laukelio verba stovėjo", "1:09", "https://www.youtube.com/watch?v=T5pSqxL4Hps"),
    ("Uoj ūžkit, ūžkit", "1:38", "https://www.youtube.com/watch?v=OxW9J0tvOZE"),
    ("Tu, lapela langvapėde", "0:27", "https://www.youtube.com/watch?v=CccYzDALFeQ"),
    ("Instrumentinė muzika / Instrumental music", "5:40", "https://www.youtube.com/watch?v=X8Nlnb-vpb4"),
    ("Šeinas", "1:25", "https://www.youtube.com/watch?v=GaxAqqLA1Hw"),
    ("Ak, bruoli bruoli", "1:22", "https://www.youtube.com/watch?v=dgSungcRS0k"),
    ("Dambrelis ir kanklės", "0:52", "https://www.youtube.com/watch?v=An20KK2QHsY"),
    ("Smuikų polka", "1:26", "https://www.youtube.com/watch?v=zbqVtQ1So8Y"),
    ("Liaudiški žaidimai", "3:04", "https://www.youtube.com/watch?v=mQ8ONDD33w8"),
    ("Maršas", "0:57", "https://www.youtube.com/watch?v=o1V5yzx109Y"),
    ("Fokstrotas", "0:49", "https://www.youtube.com/watch?v=lZScjB2-sPc"),
    ("Čitijanka", "0:56", "https://www.youtube.com/watch?v=uzdeOV-nVuM"),
    ("Polka \"Tumba tumba\"", "1:04", "https://www.youtube.com/watch?v=uIUF7RBYteA"),
    ("Polka", "1:23", "https://www.youtube.com/watch?v=A1rNkjysOUc"),
    ("Gudyno polka", "1:39", "https://www.youtube.com/watch?v=rwm5B0zcbRc"),
]

REGIONS = ['Aukštaitija', 'Žemaitija', 'Suvalkija', 'Dzūkija', 'Mažoji Lietuva']
FEATURE_TITLES = [
    "Užstalės", "Vakaronei", "Susidainavimams", "Rasoms",
    "Kalėdoms", "Adventui", "Velykoms", "Pradžia"
]

def create_features():
    for title in FEATURE_TITLES:
        Feature.objects.get_or_create(title=title)

def main():
    create_features()
    features = list(Feature.objects.all())
    ensembles = list(Ensemble.objects.all())

    for title, duration, url in PIECES:
        piece = Piece.objects.create(
            title=title,
            type="Instrumentalas",
            speed=random.choice(['Lėtas', 'Vidutinis', 'Greitas']),
            preparation=random.choice(['Naujas', 'Ruošiamas', 'Paruoštas']),
            duration=duration,
            youtube_url=url,
            description="Auto-generated from Ratilio playlist.",
            region=random.choice(REGIONS)
        )

        piece.features.set(random.sample(features, 5))
        piece.ensembles.set(random.sample(ensembles, 8))

        print(f"Created: {title}")

if __name__ == "__main__":
    main()
