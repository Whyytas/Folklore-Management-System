from django.contrib.auth.decorators import login_required
from django.urls import reverse, NoReverseMatch
from django.shortcuts import render
from django.http import JsonResponse

from Ensembles.models import Ensemble
from Events.models import Event
from Rehearsals.models import Rehearsal

MODEL_COLORS = {
    "Renginiai": "#ff0000",
    "Repeticijos": "#28a745",
    "Kita": "#ffc107",
}


@login_required
def calendar_view(request):
    user = request.user
    is_admin = getattr(user, "role", "").lower() == "administratorius"
    all_ensembles = Ensemble.objects.all() if is_admin else Ensemble.objects.filter(members=user)
    selected_ansamblis_id = request.session.get("selected_ansamblis_id")

    return render(request, "calendar.html", {
        "all_ensembles": all_ensembles,
        "selected_ansamblis_id": selected_ansamblis_id
    })


@login_required
def calendar_events(request):
    user = request.user
    is_admin = getattr(user, "role", "").lower() == "administratorius"
    events = []

    selected_ensemble_id = request.session.get("selected_ensemble_id")

    allowed_ensembles = Ensemble.objects.all() if is_admin else Ensemble.objects.filter(members=user)
    if selected_ensemble_id and allowed_ensembles.filter(id=selected_ensemble_id).exists():
        allowed_ensembles = allowed_ensembles.filter(id=selected_ensemble_id)

    # Renginiai
    events_qs = Event.objects.filter(ensemble__in=allowed_ensembles)
    for event in events_qs:
        event_color = MODEL_COLORS.get("Renginiai", "#ffc107")
        try:
            event_url = reverse('renginiai_detail', kwargs={'pk': event.pk})
        except NoReverseMatch:
            event_url = "#"

        events.append({
            "title": event.title,
            "start": event.date.isoformat(),
            "url": event_url,
            "extendedProps": {
                "type": "Renginys",
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        })

    # Repeticijos
    rehearsals_qs = Rehearsal.objects.filter(ensemble__in=allowed_ensembles)
    for rehearsal in rehearsals_qs:
        event_color = MODEL_COLORS.get("Repeticijos", "#ffc107")
        try:
            event_url = reverse('repeticija_detail', kwargs={'pk': rehearsal.pk})
        except NoReverseMatch:
            event_url = "#"

        events.append({
            "title": rehearsal.title,
            "start": rehearsal.date.isoformat(),
            "url": event_url,
            "extendedProps": {
                "type": "Repeticija",
                "color": event_color
            },
            "backgroundColor": event_color,
            "borderColor": event_color,
            "textColor": "#ffffff"
        })

    return JsonResponse(events, safe=False)
