from itertools import chain

from django.shortcuts import render, redirect
from django.utils.timezone import now

from Ensembles.models import Ensemble
from Instruments.models import Instrument
from Pieces.models import Piece
from Events.models import Event
from Rehearsals.models import Rehearsal
from datetime import datetime


def main_page(request):
    ensemble_id = request.GET.get('ensemble_id') or request.session.get("selected_ensemble_id")
    all_ensembles = Ensemble.objects.all()

    events_qs = Event.objects.filter(date__gte=now()).select_related("ensemble")
    rehearsals_qs = Rehearsal.objects.filter(date__gte=now()).select_related("ensemble")
    instruments_qs = Instrument.objects.all().select_related("ensemble")
    pieces_qs = Piece.objects.prefetch_related("ensembles")

    if ensemble_id:
        try:
            ensemble_id = int(ensemble_id)
        except ValueError:
            ensemble_id = None

        if ensemble_id:
            events_qs = events_qs.filter(ensemble_id=ensemble_id)
            rehearsals_qs = rehearsals_qs.filter(ensemble_id=ensemble_id)
            instruments_qs = instruments_qs.filter(ensemble_id=ensemble_id)
            pieces_qs = pieces_qs.filter(ensembles__id=ensemble_id)

    events = events_qs.order_by('date')[:5]
    rehearsals = rehearsals_qs.order_by('date')[:5]

    events_combined = sorted(
        chain(events, rehearsals),
        key=lambda e: getattr(e, 'date', getattr(e, 'date', datetime.min))
    )[:5]

    newest_pieces = pieces_qs.order_by('-created_at').distinct()[:5]
    newest_instruments = instruments_qs.order_by('-id')[:5]

    context = {
        'events': events_combined,
        'pieces': newest_pieces,
        'instruments': newest_instruments,
        'all_ensembles': all_ensembles,
    }
    return render(request, 'main.html', context)

def set_selected_ensemble(request):
    if request.method == "GET":
        ensemble_id = request.GET.get("ensemble_id")
        request.session["selected_ensemble_id"] = ensemble_id or None  # Save or clear
        next_url = request.META.get("HTTP_REFERER", "/")  # Redirect back
        return redirect(next_url)
    return redirect("/")