# scripts/populate_users.py
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FolkloreManagementSystem.settings')  # Replace this
django.setup()

from django.contrib.auth import get_user_model
from Ensembles.models import Ensemble

User = get_user_model()

MALE_NAMES = [
    "Lukas", "Mantas", "Tomas", "Dominykas", "Paulius", "Dovydas", "Justinas", "Vytautas"
]

MALE_SURNAMES = [
    "Petrauskas", "Kazlauskas", "Jankauskas", "Vaitkus", "Balčiūnas", "Zelionis", "Kavaliauskas"
]

FEMALE_NAMES = [
    "Gabija", "Austėja", "Ieva", "Eglė", "Rugilė", "Agnė", "Ugnė", "Monika", "Simona"
]

FEMALE_SURNAMES = [
    "Žukauskaitė", "Petraitytė", "Jonaitytė", "Urbonaitė", "Sabaliauskaitė", "Vaitkutė", "Balčiūnaitė"
]

def generate_phone():
    return f"+3706{random.randint(1000000, 9999999)}"

def generate_email(name, surname):
    return f"{name.lower()}.{surname.lower()}@example.lt"

def generate_username(name, surname):
    base = f"{name[:3].lower()}{surname[:3].lower()}"
    username = base
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1
    return username

def random_user(gender=None):
    if gender == "male":
        name = random.choice(MALE_NAMES)
        surname = random.choice(MALE_SURNAMES)
    elif gender == "female":
        name = random.choice(FEMALE_NAMES)
        surname = random.choice(FEMALE_SURNAMES)
    else:
        gender = random.choice(["male", "female"])
        return random_user(gender)
    return name, surname, gender

def main():
    ensembles = Ensemble.objects.all()
    for ensemble in ensembles:
        # Vadovas
        name, surname, gender = random_user()
        username = generate_username(name, surname)
        email = generate_email(name, surname)
        phone = generate_phone()

        vadovas = User.objects.create_user(
            username=username,
            password='testpassword123',
            name=name,
            surname=surname,
            email=email,
            phone_number=phone,
            role='vadovas'
        )
        vadovas.ensembles.add(ensemble)
        print(f"Vadovas created: {username}")

        # Nariai
        for _ in range(10):
            name, surname, gender = random_user()
            username = generate_username(name, surname)
            email = generate_email(name, surname)
            phone = generate_phone()

            narys = User.objects.create_user(
                username=username,
                password='testpassword123',
                name=name,
                surname=surname,
                email=email,
                phone_number=phone,
                role='narys'
            )
            narys.ensembles.add(ensemble)
        print(f"10 narys added to {ensemble.title}")

if __name__ == "__main__":
    main()
