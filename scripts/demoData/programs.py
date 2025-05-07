# scripts/populate_programs.py
import os
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FolkloreManagementSystem.settings')  # Replace!
django.setup()

from Ensembles.models import Ensemble
from Pieces.models import Piece
from Programs.models import Program, ProgramPiece  # Replace if app name differs

LITHUANIAN_CITIES = [
    "Vilnius", "Kaunas", "Klaipėda", "Šiauliai", "Panevėžys",
    "Alytus", "Marijampolė", "Utena", "Mažeikiai", "Jonava",
    "Tauragė", "Telšiai", "Ukmergė", "Visaginas", "Radviliškis",
    "Plungė", "Kėdainiai", "Druskininkai", "Palanga", "Birštonas",
    "Lazdijai", "Šilutė", "Zarasai", "Joniškis", "Molėtai",
    "Trakai", "Elektrėnai", "Rokiškis", "Šilalė", "Skuodas",
    "Varėna", "Ignalina", "Anykščiai", "Kupiškis", "Pasvalys"
]

PROGRAM_TYPES = [
    'Adventui', 'Rasoms', 'Lygiadieniui',
    'Vakaronei', 'Kaledoms', 'Velykoms', 'Susidainavimams'
]

TITLE_PATTERNS = [
    'Koncertas „{city}“',
    'Advento vakaras {city}',
    'Velykų pasitikimas {city}',
    'Vakaronė {city}',
    'Rasos šventė {city}',
    'Lygiadienis {city}',
    'Dainų vakaras {city}'
]

def random_duration():
    minutes = random.randint(30, 60)
    seconds = random.choice([0, 15, 30, 45])
    return f"{minutes}:{seconds:02d}"

def main():
    ensembles = Ensemble.objects.all()
    pieces = list(Piece.objects.all())

    for ensemble in ensembles:
        city = random.choice(LITHUANIAN_CITIES)
        used_titles = set()

        for _ in range(3):
            # Unique nice title
            pattern = random.choice([t for t in TITLE_PATTERNS if t not in used_titles])
            used_titles.add(pattern)
            title = pattern.format(city=city)

            program = Program.objects.create(
                title=title,
                type=random.choice(PROGRAM_TYPES),
                description=f"Auto-generated program for {ensemble.title}",
                duration=random_duration(),
                ensemble=ensemble
            )

            selected_pieces = random.sample(pieces, random.randint(4, 8))
            for idx, piece in enumerate(selected_pieces, start=1):
                ProgramPiece.objects.create(
                    program=program,
                    piece=piece,
                    queue=idx
                )
            print(f"✔ Created program: {title} ({ensemble.title})")

if __name__ == "__main__":
    main()
