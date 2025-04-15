from itertools import chain

from django.shortcuts import render, redirect
from django.utils.timezone import now

from Ansambliai.models import Ansamblis
from Instrumentai.models import Instrumentas
from Kuriniai.models import Kurinys
from Renginiai.models import Renginys
from Repeticijos.models import Repeticija


def main_page(request):
    ansamblis_id = request.GET.get('ansamblis_id') or request.session.get("selected_ansamblis_id")
    all_ansambliai = Ansamblis.objects.all()

    renginiai_qs = Renginys.objects.filter(data_laikas__gte=now()).select_related("ansamblis")
    repeticijos_qs = Repeticija.objects.filter(data__gte=now()).select_related("ansamblis")
    instrumentai_qs = Instrumentas.objects.all().select_related("ansamblis")
    kuriniai_qs = Kurinys.objects.prefetch_related("ansambliai")

    if ansamblis_id:
        try:
            ansamblis_id = int(ansamblis_id)
        except ValueError:
            ansamblis_id = None

        if ansamblis_id:
            renginiai_qs = renginiai_qs.filter(ansamblis_id=ansamblis_id)
            repeticijos_qs = repeticijos_qs.filter(ansamblis_id=ansamblis_id)
            instrumentai_qs = instrumentai_qs.filter(ansamblis_id=ansamblis_id)
            kuriniai_qs = kuriniai_qs.filter(ansambliai__id=ansamblis_id)

    renginiai = renginiai_qs.order_by('data_laikas')[:5]
    repeticijos = repeticijos_qs.order_by('data')[:5]

    events_combined = sorted(
        chain(renginiai, repeticijos),
        key=lambda e: getattr(e, 'data_laikas', getattr(e, 'data', None))
    )[:5]

    newest_kuriniai = kuriniai_qs.order_by('-created_at').distinct()[:5]
    newest_instrumentai = instrumentai_qs.order_by('-id')[:5]

    context = {
        'events': events_combined,
        'kuriniai': newest_kuriniai,
        'instrumentai': newest_instrumentai,
        'all_ansambliai': all_ansambliai,
    }
    return render(request, 'main.html', context)
def set_selected_ansamblis(request):
    if request.method == "GET":
        ansamblis_id = request.GET.get("ansamblis_id")
        request.session["selected_ansamblis_id"] = ansamblis_id or None  # Save or clear
        next_url = request.META.get("HTTP_REFERER", "/")  # Redirect back
        return redirect(next_url)
    return redirect("/")