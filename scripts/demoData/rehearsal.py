# scripts/populate_rehearsals.py
import os
import django
import random
from datetime import datetime, timedelta
from django.utils.timezone import now

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FolkloreManagementSystem.settings')
django.setup()

from Pieces.models import Piece
from Ensembles.models import Ensemble
from Rehearsals.models import Rehearsal, RehearsalPiece

TITLE_BASES = [
    "Pasiruošimas koncertui",
    "Pasiruošimas vakaronei",
    "Pasiruošimas susidainavimams",
    "Mokymai naujiems nariams",
    "Teminė repeticija",
    "Repeticija su svečiais"
]

def random_datetime_in_day(base_date):
    hour = random.randint(9, 20)
    minute = random.choice([0, 15, 30, 45])
    return base_date.replace(hour=hour, minute=minute)

def main():
    ensembles = Ensemble.objects.all()
    pieces = list(Piece.objects.all())
    today = now().date()
    may8 = datetime(2025, 5, 8)

    for ensemble in ensembles:
        titles_available = TITLE_BASES.copy()

        # 3 rehearsals AFTER May 8, 2025
        for _ in range(3):
            base_date = may8 + timedelta(days=random.randint(1, 30))
            date_time = random_datetime_in_day(base_date)

            base_title = titles_available.pop(random.randint(0, len(titles_available) - 1))
            rehearsal = Rehearsal.objects.create(
                title=base_title,
                date=date_time,
                ensemble=ensemble
            )

            for order, piece in enumerate(random.sample(pieces, 4), start=1):
                RehearsalPiece.objects.create(
                    rehearsal=rehearsal,
                    piece=piece,
                    order=order
                )
            print(f"Future rehearsal: {base_title} for {ensemble.title}")

        # 3 rehearsals BEFORE today
        titles_available = TITLE_BASES.copy()
        for _ in range(3):
            days_ago = random.randint(5, 30)
            base_date = today - timedelta(days=days_ago)
            date_time = random_datetime_in_day(datetime.combine(base_date, datetime.min.time()))

            base_title = titles_available.pop(random.randint(0, len(titles_available) - 1))
            rehearsal = Rehearsal.objects.create(
                title=base_title,
                date=date_time,
                ensemble=ensemble
            )

            for order, piece in enumerate(random.sample(pieces, 4), start=1):
                RehearsalPiece.objects.create(
                    rehearsal=rehearsal,
                    piece=piece,
                    order=order
                )
            print(f"Past rehearsal: {base_title} for {ensemble.title}")

if __name__ == "__main__":
    main()
