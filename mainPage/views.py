from django.shortcuts import render
from django.utils.timezone import now
from itertools import chain
from operator import attrgetter

from Renginiai.models import Renginys
from Repeticijos.models import Repeticija
from Kuriniai.models import Kurinys
from Instrumentai.models import Instrumentas

def main_page(request):
    ansamblis_id = request.GET.get('ansamblis_id')

    renginiai_qs = Renginys.objects.filter(data_laikas__gte=now())
    repeticijos_qs = Repeticija.objects.filter(data__gte=now())
    instrumentai_qs = Instrumentas.objects.all()

    if ansamblis_id:
        renginiai_qs = renginiai_qs.filter(ansamblis_id=ansamblis_id)
        instrumentai_qs = instrumentai_qs.filter(ansamblis_id=ansamblis_id)

    renginiai = renginiai_qs.order_by('data_laikas')[:5]
    repeticijos = repeticijos_qs.order_by('data')[:5]

    events_combined = sorted(
        chain(renginiai, repeticijos),
        key=lambda e: getattr(e, 'data_laikas', getattr(e, 'data', None))
    )[:5]

    newest_kuriniai = Kurinys.objects.order_by('-id')[:5]
    newest_instrumentai = instrumentai_qs.order_by('-id')[:5]

    context = {
        'events': events_combined,
        'kuriniai': newest_kuriniai,
        'instrumentai': newest_instrumentai,
    }
    return render(request, 'main.html', context)
