# scripts/temp_data.py
import os
import django
from django.utils.timezone import now, timedelta
from faker import Faker
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FolkloreManagementSystem.settings")
django.setup()

from Departments.models import Department
from Ensembles.models import Ensemble
from Pieces.models import Piece, Feature
from Programs.models import Program, ProgramPiece
from Events.models import Event
from Initial.models import User
from Rehearsals.models import Rehearsal, RehearsalPiece
from Instruments.models import Instrument

fake = Faker("lt_LT")

def seed_data():
    print("🌱 Starting seed...")

    if Department.objects.exists():
        print("⚠️  Data already exists. Skipping.")
        return

    departments = [
        Department.objects.create(
            title=f"Padalinys {i+1}",
            address=fake.address(),
            phone=fake.phone_number()
        ) for i in range(50)
    ]
    print("Padaliniai sukurti")

    ensembles = [
        Ensemble.objects.create(
            title=f"Ansamblis {i+1}",
            city=fake.city(),
            department=random.choice(departments)
        ) for i in range(50)
    ]
    print("Ansambliai sukurti")

    features = [Feature.objects.create(title=title) for title in [
        "Šokiams", "Vakaronei", "Susidainavimams", "Lygiadieniui",
        "Rasoms", "Kalėdoms", "Adventui", "Jurginėms", "Kaziukui", "Pradžia"
    ]]

    pieces = []
    for i in range(50):
        piece = Piece.objects.create(
            title=f"Kūrinys {i+1}",
            type=random.choice([c[0] for c in Piece.TYPE_CHOICES]),
            speed=random.choice([c[0] for c in Piece.SPEED_CHOICES]),
            preparation=random.choice([c[0] for c in Piece.PREPARATION_CHOICES]),
            duration=f"{random.randint(1,4)}:{random.randint(0,59):02d}",
            youtube_url="https://youtube.com/watch?v=dQw4w9WgXcQ",
            lyrics=fake.text(100),
            description=fake.sentence(),
            region=random.choice(['Aukštaitija', 'Žemaitija', 'Dzūkija', 'Suvalkija', 'Mažoji Lietuva']),
            place=fake.city(),
        )
        piece.ensembles.set(random.sample(ensembles, k=random.randint(1, 3)))
        piece.features.set(random.sample(features, k=random.randint(0, 5)))
        pieces.append(piece)

    print("Kuriniai sukurti")
    programs = []
    for i in range(50):
        program = Program.objects.create(
            title=f"Programa {i+1}",
            type=random.choice([c[0] for c in Program.PROGRAM_TYPE]),
            description=fake.text(100),
            duration=f"{random.randint(5,20)}:{random.randint(0,59):02d}",
            ensemble=random.choice(ensembles)
        )
        for idx, piece in enumerate(random.sample(pieces, k=random.randint(5, 10))):
            ProgramPiece.objects.create(program=program, piece=piece, queue=idx)
        programs.append(program)

    print("Programos sukurtos")
    for i in range(50):
        Event.objects.create(
            ensemble=random.choice(ensembles),
            title=f"Renginys {i+1}",
            address=fake.address(),
            date=now() + timedelta(days=random.randint(-30, 30), hours=random.randint(0, 23)),
            program=random.choice(programs),
        )
    print("Renginiai sukurti")

    for i in range(50):
        user = User.objects.create_user(
            username=f"user{i+1}",
            password="slaptas123",
            name=fake.first_name(),
            surname=fake.last_name(),
            role="narys"
        )
        user.ensembles.set(random.sample(ensembles, k=random.randint(1, 3)))

    print("Naudotojai sukurti")
    for i in range(50):
        rehearsal = Rehearsal.objects.create(
            title=f"Repeticija {i+1}",
            date=now() + timedelta(days=random.randint(-20, 20)),
            ensemble=random.choice(ensembles)
        )
        for idx, piece in enumerate(random.sample(pieces, k=random.randint(2, 6))):
            RehearsalPiece.objects.create(rehearsal=rehearsal, piece=piece, order=idx)

    print("Repeticijos sukurtos")
    for i in range(50):
        ensemble = random.choice(ensembles)
        title = fake.word().capitalize() + f"_{i + 1}"

        Instrument.objects.create(
            title=title,
            ensemble=ensemble
        )
    print("Instrumentai sukurti")

    user = User.objects.create_user(
        username="adminas",
        password="slaptazodis",
        email="vitas.ilekis@ktu.edu",
        role="administratorius",
        name="Admin",
        surname="User"
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()

    print("Job's done!")

if __name__ == "__main__":
    seed_data()
