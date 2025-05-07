# scripts/populate_pieces.py
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FolkloreManagementSystem.settings')  # Replace with your settings module
django.setup()

from Ensembles.models import Ensemble
from Pieces.models import Piece, Feature  # Adjust this import if models are in another app

PIECES = [
    ("Jėgermaršas", "1:39", "https://www.youtube.com/watch?v=CNETYsSvHm0"),
    ("Vėjava", "1:59", "https://www.youtube.com/watch?v=KE0wvnPfnhA"),
    ("Viedars", "1:47", "https://www.youtube.com/watch?v=CFcRz-NAe_c"),
    ("Aukso galva", "1:33", "https://www.youtube.com/watch?v=vUQ0FXINb5Y"),
    ("Manietų valsas", "2:51", "https://www.youtube.com/watch?v=GiDSQEEyyDs"),
    ("Mėmelio keturkinkis", "2:39", "https://www.youtube.com/watch?v=k-5G49fkyWM"),
    ("Trijų velnių šokis", "3:00", "https://www.youtube.com/watch?v=0ixuTlGljDk"),
    ("Šiaučius", "1:45", "https://www.youtube.com/watch?v=IW9sCKsp-AY"),
    ("Trampolkis", "1:55", "https://www.youtube.com/watch?v=cGAuXn5fiyA"),
    ("Šlepoks", "1:27", "https://www.youtube.com/watch?v=OuBsOb3avIc"),
    ("Lemburgis", "2:02", "https://www.youtube.com/watch?v=hwzPC4rFUJ8"),
    ("Spridikis", "1:07", "https://www.youtube.com/watch?v=JasVBaJK25A"),
    ("Lemtetiūdis", "1:24", "https://www.youtube.com/watch?v=QaRllGv_2TM"),
    ("Dustars", "1:33", "https://www.youtube.com/watch?v=VSCPSdFwukM"),
    ("Letuks", "1:24", "https://www.youtube.com/watch?v=6bozPn_mM4w"),
    ("Vingierka", "2:25", "https://www.youtube.com/watch?v=Wzx1hThZGgs"),
    ("Insterburgo keturkinkis", "1:53", "https://www.youtube.com/watch?v=n4JAjWoeZAk"),
    ("Klaipėdos suktinis jonkelis", "2:00", "https://www.youtube.com/watch?v=3nqnf7nGgxE"),
    ("Čiornasis jonkelis", "5:09", "https://www.youtube.com/watch?v=MXTGi6ASSAI"),
]

def create_features():
    base_titles = ["Užstalės", "Vakaronei", "Susidainavimams", "Rasoms",
 "Kalėdoms", "Adventui", "Velykoms", "Pradžia"]
    for title in base_titles:
        Feature.objects.get_or_create(title=title)

def main():
    create_features()

    all_ensembles = list(Ensemble.objects.all())
    all_features = list(Feature.objects.all())

    for title, duration, url in PIECES:
        piece = Piece.objects.create(
            title=title,
            type='Šokis',
            speed=random.choice(['Lėtas', 'Vidutinis', 'Greitas']),
            preparation=random.choice(['Naujas', 'Ruošiamas', 'Paruoštas']),
            duration=duration,
            youtube_url=url,
            region=random.choice(['Aukštaitija', 'Žemaitija', 'Suvalkija',
                                  'Dzūkija', 'Mažoji Lietuva']),
            description='Iš Ratilio repertuaro'
        )

        selected_features = random.sample(all_features, 5)
        selected_ensembles = random.sample(all_ensembles, 8)

        piece.features.set(selected_features)
        piece.ensembles.set(selected_ensembles)

        print(f"Created piece: {title}")

if __name__ == "__main__":
    main()
