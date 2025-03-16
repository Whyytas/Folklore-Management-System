from django.shortcuts import render
from django.utils.timezone import now
from itertools import chain
from operator import attrgetter

from Renginiai.models import Renginys
from Repeticijos.models import Repeticija
from Kuriniai.models import Kurinys
from Instrumentai.models import Instrumentas

def main_page(request):
    renginiai = Renginys.objects.filter(data_laikas__gte=now()).order_by('data_laikas')[:5]
    repeticijos = Repeticija.objects.filter(data__gte=now()).order_by('data')[:5]

    # Combine and sort by date
    events_combined = sorted(
        chain(renginiai, repeticijos),
        key=lambda e: e.data_laikas if hasattr(e, 'data_laikas') else e.data
    )[:5]

    newest_kuriniai = Kurinys.objects.order_by('-id')[:5]
    newest_instrumentai = Instrumentas.objects.order_by('-id')[:5]

    context = {
        'events': events_combined,
        'kuriniai': newest_kuriniai,
        'instrumentai': newest_instrumentai,
    }
    return render(request, 'main.html', context)
