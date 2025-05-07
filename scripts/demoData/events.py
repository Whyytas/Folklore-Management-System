# scripts/populate_events.py
import os
import django
import random
from datetime import timedelta
from django.utils.timezone import now

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FolkloreManagementSystem.settings')  # Replace with your settings module
django.setup()

from Programs.models import Program
from Events.models import Event
from Ensembles.models import Ensemble

VENUES = [
    "Kultūros centras, {city}",
    "Miesto aikštė, {city}",
    "Senoji biblioteka, {city}",
    "Laisvės alėja 12, {city}",
    "Teatras, {city}",
    "Muziejus, {city}",
    "Pilies salė, {city}",
    "Renginių centras, {city}"
]

EVENT_TITLES = [
    "Koncertas „Miesto šventė“",
    "Vakaro programa",
    "Advento vakaras",
    "Renginys bendruomenei",
    "Pasirodymas svečiams",
    "Velykų koncertas",
    "Rasos šventė",
    "Festivalio vakaras"
]

CITIES = [
    "Vilnius", "Kaunas", "Klaipėda", "Šiauliai", "Panevėžys",
    "Alytus", "Marijampolė", "Utena", "Mažeikiai", "Jonava",
    "Tauragė", "Telšiai", "Ukmergė", "Visaginas", "Radviliškis"
]

def main():
    ensembles = Ensemble.objects.all()
    programs_by_ensemble = {
        prog.ensemble_id: [] for prog in Program.objects.exclude(ensemble__isnull=True)
    }

    for prog in Program.objects.exclude(ensemble__isnull=True):
        programs_by_ensemble[prog.ensemble_id].append(prog)

    for ensemble in ensembles:
        city = ensemble.city or random.choice(CITIES)
        program_list = programs_by_ensemble.get(ensemble.id, [])

        for i in range(2):
            date_offset = random.randint(1, 30)
            event_datetime = now() + timedelta(days=date_offset, hours=random.randint(9, 20))

            title = random.choice(EVENT_TITLES)
            address = random.choice(VENUES).format(city=city)
            program = random.choice(program_list) if program_list else None

            Event.objects.create(
                ensemble=ensemble,
                title=title,
                address=address,
                date=event_datetime,
                program=program
            )

            print(f"Event {i+1}/2 for {ensemble.title}: {title} on {event_datetime.strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()
